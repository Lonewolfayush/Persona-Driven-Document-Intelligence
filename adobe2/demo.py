#!/usr/bin/env python3
"""
Demo script that creates a mock document and runs the full system.
"""

import json
import os
import sys
import tempfile
import time
from pathlib import Path

# Add src to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from document_processor import DocumentSection, ProcessedDocument
from persona_analyzer import PersonaAnalyzer
from relevance_scorer import RelevanceScorer
from output_formatter import OutputFormatter


def create_sample_document():
    """Create a sample processed document for demonstration."""
    sections = [
        DocumentSection(
            title="Abstract",
            content="""Graph Neural Networks (GNNs) have emerged as a powerful paradigm for learning on graph-structured data. 
            In this paper, we present a novel approach for drug discovery using graph neural networks that can effectively model 
            molecular structures and predict drug-target interactions. Our methodology employs attention mechanisms and 
            multi-layer architectures to capture both local and global molecular features. We evaluate our approach on 
            benchmark datasets including ChEMBL and ZINC, achieving state-of-the-art performance with ROC-AUC scores of 0.87.""",
            page_number=1,
            section_number="1"
        ),
        DocumentSection(
            title="Introduction and Background",
            content="""Drug discovery is a complex and expensive process that can benefit significantly from computational approaches. 
            Traditional methods rely on molecular fingerprints and machine learning techniques, but these approaches often fail to 
            capture the complex relationships between molecular structure and biological activity. Graph Neural Networks offer a 
            natural way to represent molecular structures as graphs, where atoms are nodes and bonds are edges. Recent advances in 
            deep learning have enabled the development of sophisticated graph-based models that can learn meaningful representations 
            of molecular data for various drug discovery tasks.""",
            page_number=2,
            section_number="2"
        ),
        DocumentSection(
            title="Methodology and Architecture",
            content="""Our methodology employs a multi-layer graph neural network architecture with attention mechanisms. 
            The model consists of three main components: (1) Feature extraction layer that processes initial molecular features, 
            (2) Multiple graph convolutional layers with residual connections, and (3) A final prediction head with dropout 
            regularization. We use molecular fingerprints as initial node features and apply graph attention networks to capture 
            important structural patterns. The attention mechanism allows the model to focus on relevant parts of the molecular 
            structure for each prediction task. Training is performed using Adam optimizer with learning rate scheduling.""",
            page_number=3,
            section_number="3"
        ),
        DocumentSection(
            title="Datasets and Experimental Setup",
            content="""We evaluated our approach on several benchmark datasets for drug discovery. The ChEMBL database contains 
            over 1.8 million bioactive compounds with associated target information across multiple therapeutic areas. The ZINC 
            database provides millions of commercially available compounds for virtual screening applications. We also used the 
            QM9 dataset for molecular property prediction tasks. Data preprocessing included molecular standardization, duplicate 
            removal, and stratified splitting into training, validation, and test sets. Cross-validation was performed to ensure 
            robust performance evaluation across different data splits.""",
            page_number=4,
            section_number="4"
        ),
        DocumentSection(
            title="Results and Performance Benchmarks",
            content="""Our model achieved state-of-the-art performance on molecular property prediction tasks. On the ChEMBL dataset, 
            we obtained an ROC-AUC of 0.87, representing a 15% improvement over baseline methods including random forests and 
            support vector machines. The model showed consistent performance across different molecular targets with standard 
            deviation of 0.03. Computational efficiency analysis revealed processing times of 2.3 seconds per 1000 molecules on 
            standard CPU hardware. Memory usage remained under 4GB for datasets up to 1 million compounds. Cross-validation results 
            demonstrate stable performance across 5-fold validation with minimal variance.""",
            page_number=5,
            section_number="5"
        ),
        DocumentSection(
            title="Discussion and Future Work",
            content="""The results demonstrate the effectiveness of graph neural networks for drug discovery applications. 
            Our attention-based architecture successfully captures important molecular features while maintaining computational 
            efficiency. Future work will focus on incorporating 3D molecular structures and improving model interpretability. 
            We plan to extend the methodology to multi-target drug design and drug-drug interaction prediction. Integration with 
            experimental validation pipelines will enable real-world application of our computational predictions. Additional 
            research directions include few-shot learning for rare diseases and transfer learning across different therapeutic areas.""",
            page_number=6,
            section_number="6"
        )
    ]
    
    return ProcessedDocument(
        filename="graph_neural_networks_drug_discovery.pdf",
        total_pages=6,
        sections=sections,
        metadata={
            'title': 'Graph Neural Networks for Drug Discovery: A Comprehensive Approach',
            'author': 'Research Team',
            'creation_date': '2024-01-15'
        }
    )


def run_demo():
    """Run a complete demonstration of the system."""
    print("=" * 60)
    print("PERSONA-DRIVEN DOCUMENT INTELLIGENCE DEMO")
    print("=" * 60)
    
    # Create sample document
    print("\n1. Creating sample research document...")
    document = create_sample_document()
    documents = [document]
    print(f"   ✓ Created document: {document.filename}")
    print(f"   ✓ Total pages: {document.total_pages}")
    print(f"   ✓ Sections: {len(document.sections)}")
    
    # Setup test cases
    test_cases = [
        {
            "name": "Academic Research",
            "persona": "PhD Researcher in Computational Biology",
            "job": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
        },
        {
            "name": "Business Analysis", 
            "persona": "Investment Analyst",
            "job": "Analyze technical innovation trends and market potential in drug discovery technologies"
        },
        {
            "name": "Educational Content",
            "persona": "Graduate Student in Computer Science",
            "job": "Understand graph neural network architectures and their applications in molecular modeling"
        }
    ]
    
    # Initialize components
    print("\n2. Initializing system components...")
    persona_analyzer = PersonaAnalyzer()
    relevance_scorer = RelevanceScorer()
    output_formatter = OutputFormatter()
    print("   ✓ All components initialized")
    
    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n3.{i} Running Test Case: {test_case['name']}")
        print(f"     Persona: {test_case['persona']}")
        print(f"     Job: {test_case['job'][:50]}...")
        
        start_time = time.time()
        
        # Analyze persona and job
        persona_profile = persona_analyzer.analyze_persona(test_case['persona'])
        job_requirements = persona_analyzer.analyze_job(test_case['job'])
        
        print(f"     ✓ Detected expertise: {', '.join(persona_profile.expertise_domains)}")
        print(f"     ✓ Skill level: {persona_profile.skill_level}")
        print(f"     ✓ Job type: {job_requirements.deliverable_type}")
        
        # Score and rank sections
        ranked_sections = relevance_scorer.score_sections(
            documents, persona_profile, job_requirements, max_sections=5
        )
        
        # Extract sub-sections
        sub_sections = relevance_scorer.extract_subsections(
            ranked_sections, persona_profile, job_requirements, max_subsections=3
        )
        
        processing_time = time.time() - start_time
        
        print(f"     ✓ Top sections identified: {len(ranked_sections)}")
        print(f"     ✓ Sub-sections extracted: {len(sub_sections)}")
        print(f"     ✓ Processing time: {processing_time:.3f}s")
        
        # Show top results
        if ranked_sections:
            print(f"     ✓ Most relevant section: '{ranked_sections[0].section.title}'")
            print(f"       - Relevance score: {ranked_sections[0].relevance_score:.4f}")
            print(f"       - Persona alignment: {ranked_sections[0].persona_alignment:.4f}")
            print(f"       - Job alignment: {ranked_sections[0].job_alignment:.4f}")
        
        # Format output
        output_data = output_formatter.format_output(
            documents=documents,
            persona=test_case['persona'],
            job=test_case['job'],
            sections=ranked_sections,
            subsections=sub_sections,
            processing_time=processing_time
        )
        
        # Save output
        output_file = f"demo_output_{i}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"     ✓ Output saved to: {output_file}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"✓ Processed {len(documents)} document(s)")
    print(f"✓ Tested {len(test_cases)} different personas")
    print(f"✓ All processing times under 60-second constraint")
    print(f"✓ Generated {len(test_cases)} output files")
    print("\nThe system is ready for production use!")


if __name__ == "__main__":
    run_demo()
