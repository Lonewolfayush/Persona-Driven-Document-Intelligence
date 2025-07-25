#!/usr/bin/env python3
"""
Test script for the Persona-Driven Document Intelligence system.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from document_processor import DocumentProcessor
from persona_analyzer import PersonaAnalyzer
from relevance_scorer import RelevanceScorer
from output_formatter import OutputFormatter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_mock_pdf_content():
    """Create mock content for testing when no PDFs are available."""
    mock_sections = [
        {
            'title': 'Introduction to Graph Neural Networks',
            'content': '''Graph Neural Networks (GNNs) have emerged as a powerful paradigm for machine learning on graph-structured data. 
            In the context of drug discovery, GNNs can effectively model molecular structures as graphs where atoms are nodes and bonds are edges. 
            This approach has shown promising results in predicting molecular properties and drug-target interactions.''',
            'page': 1
        },
        {
            'title': 'Methodology and Architecture',
            'content': '''Our methodology employs a multi-layer graph convolutional network with attention mechanisms. 
            The model architecture consists of three main components: feature extraction, graph convolution layers, and a final prediction head. 
            We use molecular fingerprints as initial node features and apply graph attention networks to capture important structural patterns.''',
            'page': 2
        },
        {
            'title': 'Dataset Description',
            'content': '''We evaluated our approach on several benchmark datasets including ChEMBL, ZINC, and QM9. 
            ChEMBL contains over 1.8 million bioactive compounds with associated target information. 
            The ZINC database provides millions of commercially available compounds for virtual screening applications.''',
            'page': 3
        },
        {
            'title': 'Performance Evaluation and Benchmarks',
            'content': '''Our model achieved state-of-the-art performance on molecular property prediction tasks. 
            On the ChEMBL dataset, we obtained an ROC-AUC of 0.87, representing a 15% improvement over baseline methods. 
            Cross-validation results demonstrate consistent performance across different molecular targets and chemical spaces.''',
            'page': 4
        },
        {
            'title': 'Discussion and Future Work',
            'content': '''The results demonstrate the effectiveness of graph neural networks for drug discovery applications. 
            Future work will focus on incorporating 3D molecular structures and improving interpretability of the learned representations. 
            We also plan to extend the methodology to multi-target drug design and drug-drug interaction prediction.''',
            'page': 5
        }
    ]
    return mock_sections


def test_system_components():
    """Test individual system components."""
    logger.info("Testing system components...")
    
    # Test persona analyzer
    persona_analyzer = PersonaAnalyzer()
    
    test_persona = "PhD Researcher in Computational Biology"
    persona_profile = persona_analyzer.analyze_persona(test_persona)
    logger.info(f"Persona analysis: {persona_profile.role}, {persona_profile.skill_level}")
    
    test_job = "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
    job_requirements = persona_analyzer.analyze_job(test_job)
    logger.info(f"Job analysis: {job_requirements.primary_goal}")
    
    # Test with mock data if no PDFs available
    mock_sections = create_mock_pdf_content()
    
    # Create mock document structure
    from document_processor import DocumentSection, ProcessedDocument
    
    sections = []
    for mock_section in mock_sections:
        section = DocumentSection(
            title=mock_section['title'],
            content=mock_section['content'],
            page_number=mock_section['page']
        )
        sections.append(section)
    
    mock_document = ProcessedDocument(
        filename="mock_research_paper.pdf",
        total_pages=5,
        sections=sections,
        metadata={'title': 'Graph Neural Networks for Drug Discovery'}
    )
    
    documents = [mock_document]
    
    # Test relevance scorer
    relevance_scorer = RelevanceScorer()
    scored_sections = relevance_scorer.score_sections(
        documents, persona_profile, job_requirements, max_sections=5
    )
    
    logger.info(f"Scored {len(scored_sections)} sections")
    for section in scored_sections[:3]:
        logger.info(f"Section: {section.section.title}, Score: {section.relevance_score:.4f}")
    
    # Test subsection extraction
    subsections = relevance_scorer.extract_subsections(
        scored_sections, persona_profile, job_requirements, max_subsections=3
    )
    
    logger.info(f"Extracted {len(subsections)} subsections")
    
    # Test output formatter
    output_formatter = OutputFormatter()
    output_data = output_formatter.format_output(
        documents=documents,
        persona=test_persona,
        job=test_job,
        sections=scored_sections,
        subsections=subsections,
        processing_time=2.5
    )
    
    # Validate output format
    if output_formatter.validate_output_format(output_data):
        logger.info("Output format validation passed")
    else:
        logger.error("Output format validation failed")
        return False
    
    # Save test output
    output_file = "test_output.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"Test output saved to {output_file}")
    return True


def test_performance():
    """Test system performance with timing."""
    logger.info("Testing system performance...")
    
    start_time = time.time()
    
    # Run component test
    success = test_system_components()
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    logger.info(f"Total processing time: {processing_time:.2f} seconds")
    
    if processing_time > 60:
        logger.warning("Processing time exceeded 60-second constraint")
    else:
        logger.info("Processing time within 60-second constraint ✓")
    
    return success and processing_time <= 60


def main():
    """Main test function."""
    logger.info("Starting system tests...")
    
    try:
        # Test components
        if not test_system_components():
            logger.error("Component tests failed")
            sys.exit(1)
        
        # Test performance
        if not test_performance():
            logger.error("Performance tests failed")
            sys.exit(1)
        
        logger.info("All tests passed successfully! ✓")
        
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
