"""
Output formatter for generating structured JSON results.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

from document_processor import ProcessedDocument
from relevance_scorer import ScoredSection, SubSection

logger = logging.getLogger(__name__)


class OutputFormatter:
    """Formats analysis results into the required JSON structure."""
    
    def format_output(
        self,
        documents: List[ProcessedDocument],
        persona: str,
        job: str,
        sections: List[ScoredSection],
        subsections: List[SubSection],
        processing_time: float
    ) -> Dict[str, Any]:
        """
        Format the analysis results into the required JSON structure.
        
        Args:
            documents: List of processed documents
            persona: Persona description
            job: Job-to-be-done description
            sections: List of scored sections
            subsections: List of sub-sections
            processing_time: Total processing time in seconds
            
        Returns:
            Formatted output dictionary
        """
        logger.info("Formatting output JSON")
        
        # Build metadata
        metadata = {
            "input_documents": [doc.filename for doc in documents],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat(),
            "processing_time_seconds": round(processing_time, 2),
            "total_documents_processed": len(documents),
            "total_sections_analyzed": sum(len(doc.sections) for doc in documents),
            "top_sections_selected": len(sections),
            "subsections_extracted": len(subsections)
        }
        
        # Format extracted sections
        extracted_sections = []
        for scored_section in sections:
            section_data = {
                "document": scored_section.document,
                "page_number": scored_section.section.page_number,
                "section_title": scored_section.section.title,
                "importance_rank": scored_section.importance_rank,
                "relevance_score": round(scored_section.relevance_score, 4),
                "persona_alignment": round(scored_section.persona_alignment, 4),
                "job_alignment": round(scored_section.job_alignment, 4),
                "section_content": self._truncate_content(scored_section.section.content, 500),
                "section_number": scored_section.section.section_number
            }
            extracted_sections.append(section_data)
        
        # Format sub-section analysis
        subsection_analysis = []
        for subsection in subsections:
            subsection_data = {
                "document": subsection.document,
                "page_number": subsection.page_number,
                "refined_text": subsection.refined_text,
                "parent_section": subsection.parent_section,
                "relevance_score": round(subsection.relevance_score, 4)
            }
            subsection_analysis.append(subsection_data)
        
        # Build final output
        output = {
            "metadata": metadata,
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis,
            "summary": {
                "top_sections_count": len(extracted_sections),
                "subsections_count": len(subsection_analysis),
                "avg_section_relevance": round(
                    sum(s.relevance_score for s in sections) / len(sections) if sections else 0, 4
                ),
                "processing_performance": {
                    "within_time_constraint": processing_time <= 60,
                    "processing_efficiency": round(len(documents) / processing_time, 2) if processing_time > 0 else 0
                }
            }
        }
        
        logger.info(f"Formatted output with {len(extracted_sections)} sections and {len(subsection_analysis)} sub-sections")
        return output
    
    def _truncate_content(self, content: str, max_length: int = 500) -> str:
        """
        Truncate content to specified length while preserving word boundaries.
        
        Args:
            content: Text content to truncate
            max_length: Maximum length in characters
            
        Returns:
            Truncated content
        """
        if len(content) <= max_length:
            return content
        
        # Find the last complete word within the limit
        truncated = content[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # If we can preserve most of the content
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    def save_output(self, output_data: Dict[str, Any], filepath: str) -> bool:
        """
        Save output data to JSON file.
        
        Args:
            output_data: Formatted output data
            filepath: Path to save the JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Output saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving output to {filepath}: {e}")
            return False
    
    def validate_output_format(self, output_data: Dict[str, Any]) -> bool:
        """
        Validate that the output matches the required format.
        
        Args:
            output_data: Output data to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["metadata", "extracted_sections", "subsection_analysis"]
        
        for key in required_keys:
            if key not in output_data:
                logger.error(f"Missing required key: {key}")
                return False
        
        # Validate metadata structure
        metadata = output_data["metadata"]
        required_metadata_keys = [
            "input_documents", "persona", "job_to_be_done", 
            "processing_timestamp", "processing_time_seconds"
        ]
        
        for key in required_metadata_keys:
            if key not in metadata:
                logger.error(f"Missing required metadata key: {key}")
                return False
        
        # Validate extracted sections structure
        for section in output_data["extracted_sections"]:
            required_section_keys = [
                "document", "page_number", "section_title", "importance_rank"
            ]
            for key in required_section_keys:
                if key not in section:
                    logger.error(f"Missing required section key: {key}")
                    return False
        
        # Validate subsection analysis structure
        for subsection in output_data["subsection_analysis"]:
            required_subsection_keys = [
                "document", "page_number", "refined_text"
            ]
            for key in required_subsection_keys:
                if key not in subsection:
                    logger.error(f"Missing required subsection key: {key}")
                    return False
        
        logger.info("Output format validation passed")
        return True
