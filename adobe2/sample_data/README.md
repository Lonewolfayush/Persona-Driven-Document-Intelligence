# Sample Test Cases for Persona-Driven Document Intelligence

This directory contains sample inputs for testing the document intelligence system.

## Test Case 1: Academic Research
- **Documents**: 4 research papers on "Graph Neural Networks for Drug Discovery"
- **Persona**: "PhD Researcher in Computational Biology"
- **Job**: "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

### Command:
```bash
python main.py \
  --documents sample_data/research_papers/ \
  --persona "PhD Researcher in Computational Biology" \
  --job "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks" \
  --output test1_output.json
```

## Test Case 2: Business Analysis
- **Documents**: 3 annual reports from competing tech companies (2022-2024)
- **Persona**: "Investment Analyst"
- **Job**: "Analyze revenue trends, R&D investments, and market positioning strategies"

### Command:
```bash
python main.py \
  --documents sample_data/annual_reports/ \
  --persona "Investment Analyst" \
  --job "Analyze revenue trends, R&D investments, and market positioning strategies" \
  --output test2_output.json
```

## Test Case 3: Educational Content
- **Documents**: 5 chapters from organic chemistry textbooks
- **Persona**: "Undergraduate Chemistry Student"
- **Job**: "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

### Command:
```bash
python main.py \
  --documents sample_data/chemistry_textbooks/ \
  --persona "Undergraduate Chemistry Student" \
  --job "Identify key concepts and mechanisms for exam preparation on reaction kinetics" \
  --output test3_output.json
```

## Docker Usage

```bash
# Build the Docker image
docker build -t document-intelligence .

# Run with mounted data directory
docker run -v $(pwd)/sample_data:/app/data document-intelligence \
  python main.py \
  --documents /app/data/research_papers \
  --persona "PhD Researcher in Computational Biology" \
  --job "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
```

## Notes
- Place your PDF documents in the appropriate subdirectories
- The system will process all PDF files in the specified directory
- Output will be saved as JSON files in the specified format
- Processing time should be ≤60 seconds for 3-10 documents
