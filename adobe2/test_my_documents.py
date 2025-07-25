#!/usr/bin/env python3
"""
Custom test script for user's project report documents.
"""

import subprocess
import sys
import os

# Ensure we're in the right directory
os.chdir('/Users/ASUS/Desktop/adobe2')

def run_test_case(persona, job, output_file, description):
    """Run a single test case and display results."""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"Persona: {persona}")
    print(f"Job: {job}")
    print(f"Output: {output_file}")
    print("-" * 60)
    
    cmd = [
        sys.executable, 'run.py',
        '--documents', 'my_test_documents/',
        '--persona', persona,
        '--job', job,
        '--output', output_file,
        '--max-sections', '8',
        '--max-subsections', '5'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ SUCCESS!")
            print("\nOutput:")
            print(result.stdout)
            
            # Try to read and show key results
            try:
                import json
                with open(output_file, 'r') as f:
                    data = json.load(f)
                
                print(f"\n📊 RESULTS SUMMARY:")
                print(f"   Documents processed: {data['metadata']['total_documents_processed']}")
                print(f"   Sections analyzed: {data['metadata']['total_sections_analyzed']}")
                print(f"   Top sections selected: {data['metadata']['top_sections_selected']}")
                print(f"   Processing time: {data['metadata']['processing_time_seconds']}s")
                
                if data['extracted_sections']:
                    print(f"\n🏆 TOP RELEVANT SECTIONS:")
                    for i, section in enumerate(data['extracted_sections'][:3], 1):
                        print(f"   {i}. {section['section_title']} (Score: {section['relevance_score']:.4f})")
                        print(f"      Document: {section['document']}")
                        print(f"      Page: {section['page_number']}")
                        
            except Exception as e:
                print(f"Could not parse results: {e}")
                
        else:
            print("❌ FAILED!")
            print("Error output:")
            print(result.stderr)
            print("Standard output:")
            print(result.stdout)
            
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT! Process took longer than 2 minutes.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Run multiple test cases for the user's project documents."""
    
    print("🚀 TESTING PERSONA-DRIVEN DOCUMENT INTELLIGENCE")
    print("📁 Your documents: CSE Mini Project Reports")
    print("🎯 Running multiple persona scenarios...")
    
    # Test cases tailored for CSE project reports
    test_cases = [
        {
            "persona": "Computer Science Professor evaluating student projects",
            "job": "Assess project methodology, technical implementation, and results for grading",
            "output": "test_professor.json",
            "description": "Professor Evaluation Scenario"
        },
        {
            "persona": "Software Engineering Student preparing for project presentation",
            "job": "Extract key technical details, methodologies, and results to present to class",
            "output": "test_student.json", 
            "description": "Student Presentation Scenario"
        },
        {
            "persona": "Industry Mentor reviewing student work",
            "job": "Identify technical strengths, innovations, and areas for improvement in project implementation",
            "output": "test_mentor.json",
            "description": "Industry Mentor Review Scenario"
        },
        {
            "persona": "Research Coordinator compiling project summaries",
            "job": "Summarize project objectives, approaches, and outcomes for departmental reporting",
            "output": "test_coordinator.json",
            "description": "Research Coordinator Scenario"
        }
    ]
    
    # Run all test cases
    for test_case in test_cases:
        run_test_case(
            test_case["persona"],
            test_case["job"], 
            test_case["output"],
            test_case["description"]
        )
    
    print(f"\n{'='*60}")
    print("🎉 ALL TESTS COMPLETED!")
    print(f"{'='*60}")
    print("📁 Output files generated:")
    for test_case in test_cases:
        print(f"   - {test_case['output']}")
    
    print("\n💡 Next steps:")
    print("   1. Review the JSON output files to see extracted sections")
    print("   2. Try your own custom persona and job descriptions")
    print("   3. Adjust --max-sections and --max-subsections as needed")

if __name__ == "__main__":
    main()
