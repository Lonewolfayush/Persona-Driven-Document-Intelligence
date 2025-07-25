#!/usr/bin/env python3
"""
Setup script for downloading and preparing required models.
"""

import logging
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_nltk_data():
    """Download required NLTK data."""
    try:
        import nltk
        logger.info("Downloading NLTK data...")
        
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        
        logger.info("NLTK data downloaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error downloading NLTK data: {e}")
        return False


def setup_spacy_model():
    """Download and setup spaCy model."""
    try:
        import spacy
        
        # Check if model already exists
        try:
            nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model already installed")
            return True
        except OSError:
            logger.info("Installing spaCy English model...")
            
            # Try to download the model
            os.system("python -m spacy download en_core_web_sm")
            
            # Verify installation
            nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model installed successfully")
            return True
            
    except Exception as e:
        logger.warning(f"spaCy model setup failed, but system can run without it: {e}")
        return False


def verify_dependencies():
    """Verify that all required dependencies are installed."""
    required_packages = [
        'pdfplumber',
        'nltk',
        'scikit-learn',
        'numpy', 
        'transformers',
        'torch'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'scikit-learn':
                import sklearn
                logger.info(f"✓ {package} is installed")
            else:
                __import__(package)
                logger.info(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"✗ {package} is missing")
    
    if missing_packages:
        logger.error(f"Missing packages: {missing_packages}")
        logger.error("Please install missing packages using: pip install -r requirements.txt")
        return False
    
    logger.info("All required dependencies are installed")
    return True


def create_models_directory():
    """Create models directory for caching."""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    logger.info(f"Models directory created: {models_dir}")
    return models_dir


def main():
    """Main setup function."""
    logger.info("Setting up Persona-Driven Document Intelligence system...")
    
    # Verify dependencies
    if not verify_dependencies():
        sys.exit(1)
    
    # Create models directory
    create_models_directory()
    
    # Download NLTK data
    if not download_nltk_data():
        logger.warning("NLTK setup failed, but system may still work with reduced functionality")
    
    # Setup spaCy model (optional)
    setup_spacy_model()
    
    # Create sample data directory
    sample_dir = Path("sample_data")
    sample_dir.mkdir(exist_ok=True)
    logger.info(f"Sample data directory created: {sample_dir}")
    
    logger.info("Setup completed successfully!")
    logger.info("You can now run the system using: python main.py --help")


if __name__ == "__main__":
    main()
