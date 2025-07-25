# Execution Instructions

## Prerequisites
- Python 3.8 or higher
- CPU-only environment (no GPU required)
- At least 2GB RAM
- 1GB free disk space for models

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup models (one-time):**
   ```bash
   python setup_models.py
   ```

3. **Run with sample data:**
   ```bash
   python main.py \
     --documents sample_data/ \
     --persona "PhD Researcher in Computational Biology" \
     --job "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
   ```

## Docker Execution

1. **Build the image:**
   ```bash
   docker build -t document-intelligence .
   ```

2. **Run with mounted data:**
   ```bash
   docker run -v $(pwd)/sample_data:/app/data \
     document-intelligence \
     python main.py \
     --documents /app/data \
     --persona "PhD Researcher in Computational Biology" \
     --job "Prepare a comprehensive literature review"
   ```

## Test the System

Run the test suite to verify everything works:
```bash
python test_system.py
```

## Command Line Arguments

- `--documents`: Path to PDF files or directory containing PDFs
- `--persona`: Description of the user persona (role and expertise)
- `--job`: Description of the job-to-be-done
- `--output`: Output JSON file path (default: challenge1b_output.json)
- `--max-sections`: Maximum sections to extract (default: 10)
- `--max-subsections`: Maximum sub-sections per section (default: 5)

## Sample Test Cases

### Academic Research
```bash
python main.py \
  --documents research_papers/ \
  --persona "PhD Researcher in Computational Biology" \
  --job "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
```

### Business Analysis
```bash
python main.py \
  --documents annual_reports/ \
  --persona "Investment Analyst" \
  --job "Analyze revenue trends, R&D investments, and market positioning strategies"
```

### Educational Content
```bash
python main.py \
  --documents textbooks/ \
  --persona "Undergraduate Chemistry Student" \
  --job "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
```

## Performance Notes

- Processing time should be ≤60 seconds for 3-10 documents
- Model size is kept ≤1GB
- CPU-only execution (no GPU dependencies)
- No internet access required during execution

## Troubleshooting

1. **Import errors**: Run `python setup_models.py` to download required models
2. **Memory issues**: Reduce `max_sections` and `max_subsections` parameters
3. **PDF parsing errors**: Ensure PDFs are text-based (not scanned images)
4. **Slow performance**: Check that documents are reasonably sized (< 100 pages each)
