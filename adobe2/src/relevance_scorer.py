"""
Relevance scorer for ranking document sections based on persona and job requirements.
"""

import logging
import math
import re
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from document_processor import DocumentSection, ProcessedDocument
from persona_analyzer import PersonaProfile, JobRequirements

logger = logging.getLogger(__name__)


@dataclass
class ScoredSection:
    """Represents a document section with relevance scores."""
    document: str
    section: DocumentSection
    relevance_score: float
    persona_alignment: float
    job_alignment: float
    importance_rank: int


@dataclass
class SubSection:
    """Represents a sub-section within a document section."""
    document: str
    page_number: int
    refined_text: str
    parent_section: str
    relevance_score: float


class RelevanceScorer:
    """Scores and ranks document sections based on persona-job alignment."""
    
    def __init__(self):
        """Initialize the relevance scorer."""
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        # Weights for different scoring components
        self.weights = {
            'keyword_match': 0.3,
            'semantic_similarity': 0.2,
            'structural_importance': 0.2,
            'persona_alignment': 0.15,
            'job_alignment': 0.15
        }
    
    def score_sections(
        self, 
        documents: List[ProcessedDocument], 
        persona: PersonaProfile, 
        job: JobRequirements,
        max_sections: int = 10
    ) -> List[ScoredSection]:
        """
        Score and rank document sections for relevance.
        
        Args:
            documents: List of processed documents
            persona: User persona profile
            job: Job requirements
            max_sections: Maximum number of sections to return
            
        Returns:
            List of scored sections ranked by relevance
        """
        logger.info(f"Scoring sections for {len(documents)} documents")
        
        all_sections = []
        
        # Collect all sections from all documents
        for doc in documents:
            for section in doc.sections:
                all_sections.append((doc.filename, section))
        
        if not all_sections:
            logger.warning("No sections found in documents")
            return []
        
        # Prepare text corpus for TF-IDF
        section_texts = [section.content for _, section in all_sections]
        
        try:
            # Fit TF-IDF vectorizer
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(section_texts)
        except Exception as e:
            logger.warning(f"TF-IDF failed, using simpler scoring: {e}")
            tfidf_matrix = None
        
        scored_sections = []
        
        for i, (doc_name, section) in enumerate(all_sections):
            # Calculate component scores
            keyword_score = self._calculate_keyword_score(section, persona, job)
            semantic_score = self._calculate_semantic_score(section, persona, job, tfidf_matrix, i)
            structural_score = self._calculate_structural_score(section)
            persona_alignment = self._calculate_persona_alignment(section, persona)
            job_alignment = self._calculate_job_alignment(section, job)
            
            # Calculate weighted overall score
            relevance_score = (
                self.weights['keyword_match'] * keyword_score +
                self.weights['semantic_similarity'] * semantic_score +
                self.weights['structural_importance'] * structural_score +
                self.weights['persona_alignment'] * persona_alignment +
                self.weights['job_alignment'] * job_alignment
            )
            
            scored_sections.append(ScoredSection(
                document=doc_name,
                section=section,
                relevance_score=relevance_score,
                persona_alignment=persona_alignment,
                job_alignment=job_alignment,
                importance_rank=0  # Will be set after sorting
            ))
        
        # Sort by relevance score and assign ranks
        scored_sections.sort(key=lambda x: x.relevance_score, reverse=True)
        for i, scored_section in enumerate(scored_sections[:max_sections], 1):
            scored_section.importance_rank = i
        
        logger.info(f"Scored and ranked {len(scored_sections[:max_sections])} sections")
        return scored_sections[:max_sections]
    
    def extract_subsections(
        self,
        sections: List[ScoredSection],
        persona: PersonaProfile,
        job: JobRequirements,
        max_subsections: int = 5
    ) -> List[SubSection]:
        """
        Extract relevant sub-sections from the top-ranked sections.
        
        Args:
            sections: List of scored sections
            persona: User persona profile
            job: Job requirements
            max_subsections: Maximum sub-sections per section
            
        Returns:
            List of extracted sub-sections
        """
        logger.info(f"Extracting sub-sections from {len(sections)} sections")
        
        subsections = []
        
        for scored_section in sections:
            section_subsections = self._extract_section_subsections(
                scored_section, persona, job, max_subsections
            )
            subsections.extend(section_subsections)
        
        # Sort all subsections by relevance
        subsections.sort(key=lambda x: x.relevance_score, reverse=True)
        
        logger.info(f"Extracted {len(subsections)} sub-sections")
        return subsections
    
    def _calculate_keyword_score(
        self, 
        section: DocumentSection, 
        persona: PersonaProfile, 
        job: JobRequirements
    ) -> float:
        """Calculate keyword-based relevance score."""
        content_lower = section.content.lower()
        title_lower = section.title.lower()
        
        # Combine persona and job keywords
        all_keywords = persona.keywords.union(job.priority_keywords)
        
        if not all_keywords:
            return 0.0
        
        # Count keyword matches
        content_matches = sum(1 for keyword in all_keywords if keyword in content_lower)
        title_matches = sum(1 for keyword in all_keywords if keyword in title_lower)
        
        # Weight title matches higher
        total_matches = content_matches + (title_matches * 2)
        
        # Normalize by content length and keyword count
        content_words = len(content_lower.split())
        if content_words == 0:
            return 0.0
        
        score = total_matches / math.sqrt(content_words) / math.sqrt(len(all_keywords))
        return min(score, 1.0)
    
    def _calculate_semantic_score(
        self,
        section: DocumentSection,
        persona: PersonaProfile,
        job: JobRequirements,
        tfidf_matrix,
        section_index: int
    ) -> float:
        """Calculate semantic similarity score."""
        if tfidf_matrix is None:
            return 0.0
        
        try:
            # Create query from persona and job
            query_text = f"{persona.role} {' '.join(persona.focus_areas)} {job.primary_goal} {' '.join(job.information_needs)}"
            query_vector = self.tfidf_vectorizer.transform([query_text])
            
            # Calculate cosine similarity
            section_vector = tfidf_matrix[section_index:section_index+1]
            similarity = cosine_similarity(query_vector, section_vector)[0][0]
            
            return similarity
        except Exception as e:
            logger.warning(f"Semantic scoring failed: {e}")
            return 0.0
    
    def _calculate_structural_score(self, section: DocumentSection) -> float:
        """Calculate structural importance score."""
        score = 0.0
        
        # Title-based scoring
        title_lower = section.title.lower()
        
        # High-value sections
        high_value_terms = [
            'abstract', 'introduction', 'conclusion', 'summary', 'results',
            'methodology', 'methods', 'discussion', 'findings', 'analysis'
        ]
        
        for term in high_value_terms:
            if term in title_lower:
                score += 0.3
                break
        
        # Section numbering (earlier sections often more important)
        if section.section_number:
            try:
                # Extract first number
                first_num = float(section.section_number.split('.')[0])
                if first_num <= 3:  # First few sections
                    score += 0.2
            except (ValueError, IndexError):
                pass
        
        # Content length (moderate length preferred)
        content_length = len(section.content.split())
        if 50 <= content_length <= 500:
            score += 0.2
        elif content_length > 500:
            score += 0.1
        
        # Page position (earlier pages often more important)
        if section.page_number <= 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_persona_alignment(
        self, 
        section: DocumentSection, 
        persona: PersonaProfile
    ) -> float:
        """Calculate alignment with persona expertise."""
        content_lower = section.content.lower()
        title_lower = section.title.lower()
        
        score = 0.0
        
        # Check expertise domain alignment
        for domain in persona.expertise_domains:
            domain_keywords = self._get_domain_keywords(domain)
            domain_matches = sum(1 for keyword in domain_keywords 
                               if keyword in content_lower or keyword in title_lower)
            if domain_matches > 0:
                score += 0.3
        
        # Check focus area alignment
        for focus_area in persona.focus_areas:
            focus_words = focus_area.lower().split()
            if any(word in content_lower or word in title_lower for word in focus_words):
                score += 0.2
        
        # Skill level adjustment
        if persona.skill_level == 'expert':
            # Prefer technical content
            technical_terms = ['methodology', 'analysis', 'framework', 'model', 'algorithm']
            if any(term in content_lower for term in technical_terms):
                score += 0.1
        elif persona.skill_level == 'beginner':
            # Prefer introductory content
            intro_terms = ['introduction', 'overview', 'basic', 'fundamental', 'concept']
            if any(term in content_lower for term in intro_terms):
                score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_job_alignment(
        self, 
        section: DocumentSection, 
        job: JobRequirements
    ) -> float:
        """Calculate alignment with job requirements."""
        content_lower = section.content.lower()
        title_lower = section.title.lower()
        
        score = 0.0
        
        # Check primary goal alignment
        goal_words = job.primary_goal.lower().split()
        goal_matches = sum(1 for word in goal_words 
                          if word in content_lower or word in title_lower)
        if goal_matches > 0:
            score += 0.4
        
        # Check information needs alignment
        for need in job.information_needs:
            need_words = need.lower().split()
            if any(word in content_lower or word in title_lower for word in need_words):
                score += 0.2
        
        # Check deliverable type alignment
        deliverable_keywords = {
            'analysis': ['analysis', 'analyze', 'examination', 'evaluation'],
            'synthesis': ['summary', 'overview', 'compilation', 'integration'],
            'review': ['review', 'survey', 'literature', 'comprehensive'],
            'preparation': ['methodology', 'approach', 'framework', 'procedure'],
            'identification': ['key', 'important', 'significant', 'main'],
            'learning': ['concept', 'principle', 'fundamental', 'theory']
        }
        
        if job.deliverable_type in deliverable_keywords:
            keywords = deliverable_keywords[job.deliverable_type]
            if any(keyword in content_lower for keyword in keywords):
                score += 0.2
        
        return min(score, 1.0)
    
    def _extract_section_subsections(
        self,
        scored_section: ScoredSection,
        persona: PersonaProfile,
        job: JobRequirements,
        max_subsections: int
    ) -> List[SubSection]:
        """Extract sub-sections from a scored section."""
        section = scored_section.section
        content = section.content
        
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return []
        
        # Score each sentence
        sentence_scores = []
        for sentence in sentences:
            score = self._score_sentence(sentence, persona, job)
            sentence_scores.append((sentence, score))
        
        # Sort by score and take top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = sentence_scores[:max_subsections]
        
        # Create sub-sections
        subsections = []
        for i, (sentence, score) in enumerate(top_sentences):
            # Expand sentence with context
            refined_text = self._refine_sentence_with_context(sentence, sentences)
            
            subsections.append(SubSection(
                document=scored_section.document,
                page_number=section.page_number,
                refined_text=refined_text,
                parent_section=section.title,
                relevance_score=score
            ))
        
        return subsections
    
    def _score_sentence(
        self, 
        sentence: str, 
        persona: PersonaProfile, 
        job: JobRequirements
    ) -> float:
        """Score a sentence for relevance."""
        sentence_lower = sentence.lower()
        
        # Keyword matching
        all_keywords = persona.keywords.union(job.priority_keywords)
        keyword_matches = sum(1 for keyword in all_keywords if keyword in sentence_lower)
        keyword_score = min(keyword_matches / len(sentence.split()) * 2, 1.0)
        
        # Length penalty (prefer moderate length)
        length = len(sentence.split())
        if 5 <= length <= 30:
            length_score = 1.0
        elif length < 5:
            length_score = 0.5
        else:
            length_score = max(0.1, 1.0 - (length - 30) * 0.02)
        
        # Content quality indicators
        quality_score = 0.0
        quality_indicators = ['result', 'finding', 'conclusion', 'analysis', 'method', 'approach']
        if any(indicator in sentence_lower for indicator in quality_indicators):
            quality_score = 0.3
        
        return (keyword_score * 0.6) + (length_score * 0.2) + (quality_score * 0.2)
    
    def _refine_sentence_with_context(self, target_sentence: str, all_sentences: List[str]) -> str:
        """Refine a sentence by adding relevant context."""
        # Find the target sentence in the list
        target_index = -1
        for i, sentence in enumerate(all_sentences):
            if target_sentence.strip() in sentence:
                target_index = i
                break
        
        if target_index == -1:
            return target_sentence
        
        # Add context sentences (one before, one after if available)
        context_sentences = []
        
        if target_index > 0:
            context_sentences.append(all_sentences[target_index - 1])
        
        context_sentences.append(target_sentence)
        
        if target_index < len(all_sentences) - 1:
            context_sentences.append(all_sentences[target_index + 1])
        
        # Join and clean up
        refined_text = '. '.join(context_sentences)
        refined_text = re.sub(r'\s+', ' ', refined_text).strip()
        
        return refined_text
    
    def _get_domain_keywords(self, domain: str) -> List[str]:
        """Get keywords for a specific domain."""
        domain_keywords = {
            'computer_science': ['algorithm', 'programming', 'software', 'computing', 'data', 'neural', 'machine'],
            'biology': ['gene', 'protein', 'cell', 'organism', 'molecular', 'genetic'],
            'chemistry': ['reaction', 'compound', 'molecule', 'synthesis', 'organic', 'kinetics'],
            'finance': ['revenue', 'profit', 'investment', 'market', 'financial'],
            'medicine': ['patient', 'treatment', 'clinical', 'therapeutic', 'medical'],
            'research': ['study', 'analysis', 'methodology', 'experiment', 'literature'],
            'education': ['learning', 'curriculum', 'academic', 'study'],
            'business': ['strategy', 'management', 'operations', 'marketing']
        }
        
        return domain_keywords.get(domain, [])
