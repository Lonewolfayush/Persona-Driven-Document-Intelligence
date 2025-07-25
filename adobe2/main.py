#!/usr/bin/env python3
"""
Main entry point for the Persona-Driven Document Intelligence system.
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from src.document_processor import DocumentProcessor
from src.persona_analyzer import PersonaAnalyzer
from src.relevance_scorer import RelevanceScorer
from src.output_formatter import OutputFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Persona-Driven Document Intelligence System'
    )
    parser.add_argument(
        '--documents',
        type=str,
        required=True,
        help='Path to directory containing PDF documents or single PDF file'
    )
    parser.add_argument(
        '--persona',
        type=str,
        required=True,
        help='Persona description (role and expertise)'
    )
    parser.add_argument(
        '--job',
        type=str,
        required=True,
        help='Job-to-be-done description'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='challenge1b_output.json',
        help='Output JSON file path'
    )
    parser.add_argument(
        '--max-sections',
        type=int,
        default=10,
        help='Maximum number of sections to extract'
    )
    parser.add_argument(
        '--max-subsections',
        type=int,
        default=5,
        help='Maximum number of sub-sections per section'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.documents):
        logger.error(f"Documents path does not exist: {args.documents}")
        sys.exit(1)
    
    start_time = time.time()
    
    try:
        # Initialize components
        logger.info("Initializing document processing components...")
        document_processor = DocumentProcessor()
        persona_analyzer = PersonaAnalyzer()
        relevance_scorer = RelevanceScorer()
        output_formatter = OutputFormatter()
        
        # Process documents
        logger.info(f"Processing documents from: {args.documents}")
        documents = document_processor.process_documents(args.documents)
        
        if not documents:
            logger.error("No documents found or processed successfully")
            sys.exit(1)
        
        # Analyze persona and job
        logger.info("Analyzing persona and job requirements...")
        persona_profile = persona_analyzer.analyze_persona(args.persona)
        job_requirements = persona_analyzer.analyze_job(args.job)
        
        # Score and rank sections
        logger.info("Scoring document sections for relevance...")
        ranked_sections = relevance_scorer.score_sections(
            documents, persona_profile, job_requirements, args.max_sections
        )
        
        # Extract sub-sections
        logger.info("Extracting relevant sub-sections...")
        sub_sections = relevance_scorer.extract_subsections(
            ranked_sections, persona_profile, job_requirements, args.max_subsections
        )
        
        # Format output
        logger.info("Formatting output...")
        output_data = output_formatter.format_output(
            documents=documents,
            persona=args.persona,
            job=args.job,
            sections=ranked_sections,
            subsections=sub_sections,
            processing_time=time.time() - start_time
        )
        
        # Save output
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        processing_time = time.time() - start_time
        logger.info(f"Processing completed in {processing_time:.2f} seconds")
        logger.info(f"Output saved to: {args.output}")
        
        # Validate processing time constraint
        if processing_time > 60:
            logger.warning(f"Processing time ({processing_time:.2f}s) exceeded 60-second constraint")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
