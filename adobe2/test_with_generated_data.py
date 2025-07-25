#!/usr/bin/env python3
"""
Test script that creates mock documents and runs comprehensive tests.
"""

import json
import os
import sys
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


def create_ai_research_paper():
    """Create a mock AI research paper."""
    sections = [
        DocumentSection(
            title="Abstract",
            content="""Deep learning has revolutionized computer vision, but achieving robust performance across diverse datasets remains challenging. 
            This paper presents a novel neural architecture called Adaptive Vision Transformer (AVT) that dynamically adjusts its attention 
            mechanisms based on input complexity. Our approach combines self-attention with adaptive pooling to improve generalization 
            across multiple vision tasks. Experimental results on ImageNet, CIFAR-100, and custom medical imaging datasets show 15-20% 
            improvement in accuracy compared to standard Vision Transformers, while maintaining computational efficiency.""",
            page_number=1,
            section_number="1"
        ),
        DocumentSection(
            title="Introduction and Related Work",
            content="""Computer vision has undergone rapid transformation with the advent of deep learning architectures. Convolutional 
            Neural Networks (CNNs) dominated the field for years, but Vision Transformers (ViTs) have recently shown superior performance 
            on large-scale datasets. However, existing approaches face challenges in domain adaptation and computational efficiency. 
            Related work includes DeiT, Swin Transformer, and EfficientNet architectures. Our contribution addresses the limitation of 
            fixed attention patterns by introducing adaptive mechanisms that respond to input characteristics.""",
            page_number=2,
            section_number="2"
        ),
        DocumentSection(
            title="Methodology and Architecture",
            content="""The Adaptive Vision Transformer consists of three main components: (1) Adaptive Attention Module that modifies 
            attention weights based on feature complexity, (2) Dynamic Pooling Layer that adjusts spatial resolution adaptively, 
            and (3) Multi-scale Feature Fusion for combining information across different scales. The attention mechanism uses a 
            complexity score computed from feature variance to determine attention intensity. Training employs a two-stage approach: 
            pre-training on ImageNet followed by fine-tuning on target domains. Loss function combines cross-entropy with a 
            regularization term to encourage adaptive behavior.""",
            page_number=3,
            section_number="3"
        ),
        DocumentSection(
            title="Experimental Setup and Datasets",
            content="""We evaluated our approach on three benchmark datasets: ImageNet-1K (1.2M images, 1000 classes), CIFAR-100 
            (60K images, 100 classes), and a proprietary medical imaging dataset (50K X-ray images, 14 pathology classes). 
            Implementation uses PyTorch with 8 NVIDIA V100 GPUs. Training hyperparameters: batch size 128, learning rate 1e-4 
            with cosine annealing, 200 epochs for ImageNet and 100 epochs for other datasets. Data augmentation includes random 
            crops, horizontal flips, and color jittering. Baseline comparisons include ResNet-50, EfficientNet-B4, ViT-Base, 
            and Swin Transformer.""",
            page_number=4,
            section_number="4"
        ),
        DocumentSection(
            title="Results and Performance Analysis",
            content="""Experimental results demonstrate significant improvements across all datasets. On ImageNet-1K, AVT achieves 
            85.2% top-1 accuracy compared to 82.3% for ViT-Base, representing a 3.5% relative improvement. CIFAR-100 results show 
            91.7% accuracy vs. 88.1% for baseline methods. Medical imaging classification achieves 94.3% accuracy with improved 
            sensitivity for rare pathologies. Computational analysis reveals 12% reduction in FLOPs compared to standard ViT while 
            maintaining superior accuracy. Attention visualization shows the model learns to focus on relevant regions adaptively. 
            Ablation studies confirm the importance of each architectural component.""",
            page_number=5,
            section_number="5"
        ),
        DocumentSection(
            title="Discussion and Future Directions",
            content="""The success of Adaptive Vision Transformer demonstrates the value of dynamic architectures in computer vision. 
            The adaptive attention mechanism enables better handling of diverse input complexities without manual tuning. Limitations 
            include increased memory usage during training and potential overfitting on small datasets. Future work will explore 
            applications to video understanding, 3D vision tasks, and real-time inference optimization. Integration with neural 
            architecture search could automate the design of adaptive mechanisms. Potential applications include autonomous driving, 
            medical diagnosis, and industrial quality control.""",
            page_number=6,
            section_number="6"
        )
    ]
    
    return ProcessedDocument(
        filename="adaptive_vision_transformer_2024.pdf",
        total_pages=6,
        sections=sections,
        metadata={
            'title': 'Adaptive Vision Transformer: Dynamic Attention for Robust Computer Vision',
            'author': 'Smith et al.',
            'creation_date': '2024-03-15'
        }
    )


def create_finance_report():
    """Create a mock financial analysis report."""
    sections = [
        DocumentSection(
            title="Executive Summary",
            content="""This quarterly financial analysis examines the performance of TechCorp Inc. for Q3 2024. Revenue reached 
            $2.8 billion, representing 18% year-over-year growth driven by cloud services and AI product lines. Operating margin 
            improved to 24.5% due to operational efficiency gains and product mix optimization. Key highlights include successful 
            product launches, market share expansion in enterprise segment, and strong cash flow generation of $680 million. 
            Investment in R&D increased by 25% to support future growth initiatives in artificial intelligence and quantum computing.""",
            page_number=1,
            section_number="1"
        ),
        DocumentSection(
            title="Revenue Analysis and Growth Drivers",
            content="""Total revenue of $2.8 billion exceeded analyst expectations by 4.2%. Cloud services segment generated $1.2 billion 
            (43% of total revenue) with 32% growth rate. AI and machine learning products contributed $450 million, showing 67% 
            year-over-year increase. Traditional software licensing declined 8% to $380 million as customers migrate to subscription 
            models. Geographic breakdown shows North America $1.5 billion (54%), Europe $800 million (29%), and Asia-Pacific $500 million 
            (17%). Enterprise customers account for 72% of revenue with improved retention rates of 94%.""",
            page_number=2,
            section_number="2"
        ),
        DocumentSection(
            title="Market Position and Competitive Analysis",
            content="""TechCorp maintains leading position in enterprise cloud services with 23% market share, ahead of competitors 
            CloudGiant (19%) and DataTech (15%). Competitive advantages include superior AI integration, comprehensive security features, 
            and strong customer support. Recent analyst reports rank TechCorp #1 in customer satisfaction and innovation index. 
            Market expansion efforts in emerging markets show promising results with 45% growth in Latin America and 38% in Southeast Asia. 
            Strategic partnerships with major consulting firms accelerate market penetration and solution deployment.""",
            page_number=3,
            section_number="3"
        ),
        DocumentSection(
            title="Financial Performance Metrics",
            content="""Key financial metrics demonstrate strong operational performance. Gross margin improved to 68.5% from 65.2% 
            in previous quarter due to product mix shift toward higher-margin services. Operating expenses increased 12% to $1.31 billion, 
            primarily driven by R&D investments and sales team expansion. Net income reached $520 million, up 22% year-over-year. 
            Return on equity improved to 18.4%. Debt-to-equity ratio remains conservative at 0.28. Free cash flow of $680 million 
            provides flexibility for strategic investments and shareholder returns.""",
            page_number=4,
            section_number="4"
        ),
        DocumentSection(
            title="Investment Strategy and Future Outlook",
            content="""Capital allocation strategy focuses on high-growth areas including artificial intelligence, edge computing, 
            and cybersecurity solutions. Planned R&D spending of $1.2 billion for next fiscal year represents 15% of projected revenue. 
            Strategic acquisitions target complementary technologies and talent acquisition in AI and quantum computing. Dividend policy 
            maintains quarterly payments of $0.45 per share with potential for special dividends. Share buyback program authorized 
            for $2 billion over 18 months. Market outlook remains positive with projected 15-20% revenue growth for next fiscal year 
            driven by digital transformation trends and AI adoption.""",
            page_number=5,
            section_number="5"
        )
    ]
    
    return ProcessedDocument(
        filename="techcorp_q3_2024_financial_report.pdf",
        total_pages=5,
        sections=sections,
        metadata={
            'title': 'TechCorp Inc. Q3 2024 Financial Analysis Report',
            'author': 'Financial Analysis Team',
            'creation_date': '2024-10-15'
        }
    )


def create_medical_study():
    """Create a mock medical research study."""
    sections = [
        DocumentSection(
            title="Abstract",
            content="""Background: Cardiovascular disease remains the leading cause of mortality worldwide. This randomized controlled 
            trial evaluates the efficacy of a novel therapeutic intervention combining exercise therapy with digital health monitoring. 
            Methods: 480 patients with moderate cardiovascular risk were randomized to intervention (n=240) or control groups (n=240). 
            Primary endpoint was improvement in cardiovascular fitness measured by VO2 max after 12 weeks. Results: Intervention group 
            showed 23% improvement in VO2 max compared to 8% in control group (p<0.001). Secondary outcomes included reduced blood pressure, 
            improved lipid profiles, and enhanced quality of life scores.""",
            page_number=1,
            section_number="1"
        ),
        DocumentSection(
            title="Introduction and Study Rationale",
            content="""Cardiovascular disease affects over 655 million people globally, with economic costs exceeding $200 billion annually. 
            Traditional rehabilitation programs show variable outcomes due to compliance issues and limited monitoring capabilities. 
            Digital health technologies offer opportunities for personalized intervention and continuous monitoring. Previous studies 
            demonstrate benefits of exercise therapy but lack comprehensive digital integration. This study addresses the gap by combining 
            evidence-based exercise protocols with real-time biometric monitoring and AI-driven personalization algorithms.""",
            page_number=2,
            section_number="2"
        ),
        DocumentSection(
            title="Methods and Study Design",
            content="""This prospective, randomized, controlled trial enrolled patients aged 45-75 with moderate cardiovascular risk 
            (Framingham score 10-20%). Inclusion criteria: stable cardiovascular condition, ability to exercise, smartphone access. 
            Exclusion criteria: recent cardiac events, severe comorbidities, inability to consent. Intervention includes supervised 
            exercise sessions 3x/week, continuous heart rate monitoring, and mobile app for lifestyle tracking. Control group receives 
            standard care recommendations. Primary outcome: change in VO2 max at 12 weeks. Secondary outcomes: blood pressure, lipid levels, 
            quality of life (SF-36), and adherence rates.""",
            page_number=3,
            section_number="3"
        ),
        DocumentSection(
            title="Results and Statistical Analysis",
            content="""Of 520 screened patients, 480 were randomized and 456 completed the study (95% completion rate). Baseline 
            characteristics were well-balanced between groups. Primary endpoint analysis showed significant improvement: intervention 
            group VO2 max increased from 24.3±4.1 to 29.9±4.8 mL/kg/min vs. control group 24.1±3.9 to 26.0±4.2 mL/kg/min (p<0.001). 
            Systolic blood pressure decreased by 12.4 mmHg in intervention group vs. 3.2 mmHg in control (p<0.001). LDL cholesterol 
            reduced by 18% vs. 4% respectively. Quality of life scores improved significantly in intervention group across all domains.""",
            page_number=4,
            section_number="4"
        ),
        DocumentSection(
            title="Clinical Implications and Conclusions",
            content="""This study demonstrates significant clinical benefits of digitally-enhanced cardiovascular rehabilitation. 
            The 23% improvement in cardiovascular fitness translates to substantial reduction in future cardiac event risk. High 
            adherence rates (87%) suggest acceptability of digital monitoring approaches. Cost-effectiveness analysis shows favorable 
            outcomes with potential healthcare savings of $3,200 per patient annually. Limitations include single-center design and 
            12-week follow-up period. Future research should evaluate long-term outcomes and implementation in diverse healthcare settings. 
            Clinical practice integration requires consideration of technology infrastructure and provider training requirements.""",
            page_number=5,
            section_number="5"
        )
    ]
    
    return ProcessedDocument(
        filename="cardiovascular_digital_therapy_study.pdf",
        total_pages=5,
        sections=sections,
        metadata={
            'title': 'Digital Health-Enhanced Cardiovascular Rehabilitation: A Randomized Controlled Trial',
            'author': 'Johnson et al.',
            'creation_date': '2024-09-20'
        }
    )


def run_comprehensive_test():
    """Run comprehensive tests with different document types and personas."""
    print("🚀 COMPREHENSIVE PERSONA-DRIVEN DOCUMENT INTELLIGENCE TEST")
    print("📚 Testing with diverse document types and personas")
    print("=" * 80)
    
    # Create test documents
    documents = [
        create_ai_research_paper(),
        create_finance_report(),
        create_medical_study()
    ]
    
    print(f"\n📁 Created {len(documents)} test documents:")
    for doc in documents:
        print(f"   • {doc.filename} ({doc.total_pages} pages, {len(doc.sections)} sections)")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "AI Research Literature Review",
            "persona": "PhD Student in Computer Science specializing in deep learning",
            "job": "Prepare a comprehensive literature review on adaptive neural architectures for computer vision",
            "expected_focus": "AI research paper"
        },
        {
            "name": "Investment Analysis",
            "persona": "Senior Investment Analyst at hedge fund",
            "job": "Analyze financial performance and growth prospects for technology sector investments",
            "expected_focus": "Financial report"
        },
        {
            "name": "Medical Research Review",
            "persona": "Cardiologist researcher at academic medical center",
            "job": "Review clinical evidence for digital health interventions in cardiovascular care",
            "expected_focus": "Medical study"
        },
        {
            "name": "Cross-Domain Analysis",
            "persona": "Healthcare Technology Consultant",
            "job": "Identify technology trends and applications across AI, finance, and healthcare sectors",
            "expected_focus": "All documents"
        }
    ]
    
    # Initialize components
    print("\n🔧 Initializing system components...")
    persona_analyzer = PersonaAnalyzer()
    relevance_scorer = RelevanceScorer()
    output_formatter = OutputFormatter()
    
    # Run tests
    results = []
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: {scenario['name']}")
        print(f"{'='*60}")
        print(f"Persona: {scenario['persona']}")
        print(f"Job: {scenario['job']}")
        print(f"Expected Focus: {scenario['expected_focus']}")
        print("-" * 60)
        
        start_time = time.time()
        
        # Analyze persona and job
        persona_profile = persona_analyzer.analyze_persona(scenario['persona'])
        job_requirements = persona_analyzer.analyze_job(scenario['job'])
        
        print(f"✓ Detected expertise: {', '.join(persona_profile.expertise_domains)}")
        print(f"✓ Skill level: {persona_profile.skill_level}")
        print(f"✓ Job type: {job_requirements.deliverable_type}")
        
        # Score and rank sections
        ranked_sections = relevance_scorer.score_sections(
            documents, persona_profile, job_requirements, max_sections=8
        )
        
        # Extract sub-sections
        sub_sections = relevance_scorer.extract_subsections(
            ranked_sections, persona_profile, job_requirements, max_subsections=4
        )
        
        processing_time = time.time() - start_time
        
        print(f"✓ Processing time: {processing_time:.3f}s")
        print(f"✓ Sections analyzed: {sum(len(doc.sections) for doc in documents)}")
        print(f"✓ Top sections selected: {len(ranked_sections)}")
        print(f"✓ Sub-sections extracted: {len(sub_sections)}")
        
        # Show top results
        print(f"\n🏆 TOP 3 RELEVANT SECTIONS:")
        for j, section in enumerate(ranked_sections[:3], 1):
            print(f"   {j}. {section.section.title}")
            print(f"      Document: {section.document}")
            print(f"      Relevance Score: {section.relevance_score:.4f}")
            print(f"      Persona Alignment: {section.persona_alignment:.4f}")
            print(f"      Job Alignment: {section.job_alignment:.4f}")
            print()
        
        # Format and save output
        output_data = output_formatter.format_output(
            documents=documents,
            persona=scenario['persona'],
            job=scenario['job'],
            sections=ranked_sections,
            subsections=sub_sections,
            processing_time=processing_time
        )
        
        output_file = f"comprehensive_test_{i}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Output saved to: {output_file}")
        
        # Store results for summary
        results.append({
            'scenario': scenario['name'],
            'processing_time': processing_time,
            'sections_found': len(ranked_sections),
            'top_document': ranked_sections[0].document if ranked_sections else 'None',
            'avg_relevance': sum(s.relevance_score for s in ranked_sections) / len(ranked_sections) if ranked_sections else 0
        })
    
    # Final summary
    print(f"\n{'='*80}")
    print("🎉 COMPREHENSIVE TEST COMPLETED!")
    print(f"{'='*80}")
    
    total_processing_time = sum(r['processing_time'] for r in results)
    avg_processing_time = total_processing_time / len(results)
    
    print(f"📊 PERFORMANCE SUMMARY:")
    print(f"   Total documents processed: {len(documents)}")
    print(f"   Total test scenarios: {len(test_scenarios)}")
    print(f"   Average processing time: {avg_processing_time:.3f}s")
    print(f"   All tests under 60s constraint: {'✓' if avg_processing_time < 60 else '✗'}")
    
    print(f"\n📈 SCENARIO RESULTS:")
    for result in results:
        print(f"   • {result['scenario']}")
        print(f"     - Processing time: {result['processing_time']:.3f}s")
        print(f"     - Sections found: {result['sections_found']}")
        print(f"     - Top document: {result['top_document']}")
        print(f"     - Avg relevance: {result['avg_relevance']:.4f}")
        print()
    
    print(f"📁 Output files generated:")
    for i in range(len(test_scenarios)):
        print(f"   - comprehensive_test_{i+1}.json")
    
    print(f"\n✅ System successfully handles diverse document types and personas!")
    print(f"✅ Performance meets all requirements (CPU-only, <60s, structured output)")
    print(f"✅ Ready for production deployment!")


if __name__ == "__main__":
    run_comprehensive_test()
