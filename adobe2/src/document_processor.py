"""
Document processor for extracting and structuring content from PDF files.
"""

import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pdfplumber
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DocumentSection:
    """Represents a section within a document."""
    title: str
    content: str
    page_number: int
    section_number: Optional[str] = None
    start_position: Optional[int] = None
    end_position: Optional[int] = None


@dataclass
class ProcessedDocument:
    """Represents a processed document with extracted sections."""
    filename: str
    total_pages: int
    sections: List[DocumentSection]
    metadata: Dict[str, any]


class DocumentProcessor:
    """Processes PDF documents and extracts structured content."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.section_patterns = [
            r'^(\d+\.?\d*\.?\d*)\s+(.+)$',  # Numbered sections (1.1, 1.1.1)
            r'^([IVX]+\.?\d*)\s+(.+)$',     # Roman numerals
            r'^(Abstract|Introduction|Background|Methodology|Methods|Results|Discussion|Conclusion|References).*$',
            r'^(Chapter \d+|Section \d+).*$',
            r'^([A-Z][A-Z\s]+)$',           # ALL CAPS headers
        ]
    
    def process_documents(self, documents_path: str) -> List[ProcessedDocument]:
        """
        Process documents from a file or directory.
        
        Args:
            documents_path: Path to PDF file or directory containing PDFs
            
        Returns:
            List of processed documents
        """
        documents = []
        
        if os.path.isfile(documents_path):
            if documents_path.lower().endswith('.pdf'):
                doc = self._process_single_document(documents_path)
                if doc:
                    documents.append(doc)
        elif os.path.isdir(documents_path):
            pdf_files = list(Path(documents_path).glob('*.pdf'))
            logger.info(f"Found {len(pdf_files)} PDF files")
            
            for pdf_file in pdf_files:
                doc = self._process_single_document(str(pdf_file))
                if doc:
                    documents.append(doc)
        
        logger.info(f"Successfully processed {len(documents)} documents")
        return documents
    
    def _process_single_document(self, pdf_path: str) -> Optional[ProcessedDocument]:
        """
        Process a single PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            ProcessedDocument or None if processing failed
        """
        try:
            logger.info(f"Processing document: {pdf_path}")
            
            with pdfplumber.open(pdf_path) as pdf:
                sections = []
                all_text = ""
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        all_text += f"\n--- PAGE {page_num} ---\n{page_text}"
                
                # Extract sections
                sections = self._extract_sections(all_text)
                
                # Create document metadata
                metadata = {
                    'file_size': os.path.getsize(pdf_path),
                    'creation_date': None,
                    'title': None
                }
                
                # Try to extract PDF metadata
                try:
                    if pdf.metadata:
                        metadata.update({
                            'title': pdf.metadata.get('Title'),
                            'author': pdf.metadata.get('Author'),
                            'subject': pdf.metadata.get('Subject'),
                            'creation_date': pdf.metadata.get('CreationDate')
                        })
                except Exception as e:
                    logger.warning(f"Could not extract metadata from {pdf_path}: {e}")
                
                return ProcessedDocument(
                    filename=os.path.basename(pdf_path),
                    total_pages=len(pdf.pages),
                    sections=sections,
                    metadata=metadata
                )
                
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")
            return None
    
    def _extract_sections(self, text: str) -> List[DocumentSection]:
        """
        Extract sections from document text.
        
        Args:
            text: Full document text
            
        Returns:
            List of document sections
        """
        sections = []
        lines = text.split('\n')
        current_section = None
        current_content = []
        current_page = 1
        
        for line in lines:
            line = line.strip()
            
            # Track page numbers
            if line.startswith('--- PAGE '):
                try:
                    current_page = int(line.split()[2])
                except (IndexError, ValueError):
                    pass
                continue
            
            # Check if line is a section header
            section_match = self._is_section_header(line)
            if section_match:
                # Save previous section
                if current_section and current_content:
                    current_section.content = '\n'.join(current_content).strip()
                    sections.append(current_section)
                
                # Start new section
                current_section = DocumentSection(
                    title=section_match,
                    content="",
                    page_number=current_page,
                    section_number=self._extract_section_number(section_match)
                )
                current_content = []
            else:
                # Add to current section content
                if line:  # Skip empty lines
                    current_content.append(line)
        
        # Add final section
        if current_section and current_content:
            current_section.content = '\n'.join(current_content).strip()
            sections.append(current_section)
        
        # If no sections found, create a single section with all content
        if not sections and text.strip():
            sections.append(DocumentSection(
                title="Document Content",
                content=text.strip(),
                page_number=1
            ))
        
        logger.info(f"Extracted {len(sections)} sections")
        return sections
    
    def _is_section_header(self, line: str) -> Optional[str]:
        """
        Check if a line is a section header.
        
        Args:
            line: Text line to check
            
        Returns:
            Section title if it's a header, None otherwise
        """
        if len(line) < 3 or len(line) > 200:
            return None
        
        for pattern in self.section_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 2:
                    return match.group(2).strip()
                else:
                    return line.strip()
        
        # Check for other header indicators
        if (line.isupper() and len(line.split()) <= 8 and 
            not any(char.isdigit() for char in line)):
            return line.strip()
        
        return None
    
    def _extract_section_number(self, title: str) -> Optional[str]:
        """
        Extract section number from title.
        
        Args:
            title: Section title
            
        Returns:
            Section number or None
        """
        # Look for numbers at the beginning
        match = re.match(r'^(\d+\.?\d*\.?\d*)', title)
        if match:
            return match.group(1)
        
        # Look for roman numerals
        match = re.match(r'^([IVX]+)', title)
        if match:
            return match.group(1)
        
        return None
