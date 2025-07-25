"""
Persona analyzer for understanding user roles, expertise, and job requirements.
"""

import logging
import re
from typing import Dict, List, Set
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PersonaProfile:
    """Represents a user persona with expertise and focus areas."""
    role: str
    expertise_domains: List[str]
    focus_areas: List[str]
    skill_level: str  # beginner, intermediate, advanced, expert
    keywords: Set[str]


@dataclass
class JobRequirements:
    """Represents job-to-be-done requirements."""
    primary_goal: str
    information_needs: List[str]
    deliverable_type: str
    priority_keywords: Set[str]
    success_criteria: List[str]


class PersonaAnalyzer:
    """Analyzes persona descriptions and job requirements."""
    
    def __init__(self):
        """Initialize the persona analyzer."""
        # Domain knowledge mappings
        self.domain_keywords = {
            'computer_science': ['algorithm', 'programming', 'software', 'computing', 'data structure', 'AI', 'ML', 'neural network'],
            'biology': ['gene', 'protein', 'cell', 'organism', 'evolution', 'molecular', 'biochemistry', 'genetics'],
            'chemistry': ['reaction', 'compound', 'molecule', 'synthesis', 'organic', 'inorganic', 'kinetics', 'thermodynamics'],
            'finance': ['revenue', 'profit', 'investment', 'market', 'financial', 'economics', 'trading', 'portfolio'],
            'medicine': ['patient', 'treatment', 'diagnosis', 'clinical', 'therapeutic', 'medical', 'healthcare', 'disease'],
            'research': ['study', 'analysis', 'methodology', 'experiment', 'hypothesis', 'literature', 'peer review', 'publication'],
            'education': ['student', 'learning', 'curriculum', 'teaching', 'academic', 'exam', 'course', 'study'],
            'business': ['strategy', 'management', 'operations', 'marketing', 'sales', 'customer', 'competitive', 'market']
        }
        
        # Role skill level indicators
        self.skill_indicators = {
            'beginner': ['student', 'undergraduate', 'learner', 'new', 'entry-level'],
            'intermediate': ['graduate', 'analyst', 'associate', 'junior'],
            'advanced': ['senior', 'manager', 'specialist', 'experienced'],
            'expert': ['phd', 'professor', 'director', 'principal', 'chief', 'lead', 'expert']
        }
        
        # Job type mappings
        self.job_types = {
            'analysis': ['analyze', 'analysis', 'examine', 'evaluate', 'assess', 'compare'],
            'synthesis': ['summarize', 'compile', 'integrate', 'combine', 'consolidate'],
            'review': ['review', 'survey', 'overview', 'comprehensive', 'literature'],
            'preparation': ['prepare', 'create', 'develop', 'design', 'build'],
            'identification': ['identify', 'find', 'locate', 'extract', 'select'],
            'learning': ['learn', 'study', 'understand', 'master', 'practice']
        }
    
    def analyze_persona(self, persona_description: str) -> PersonaProfile:
        """
        Analyze persona description to extract profile information.
        
        Args:
            persona_description: Text description of the persona
            
        Returns:
            PersonaProfile object
        """
        logger.info(f"Analyzing persona: {persona_description}")
        
        # Extract role
        role = self._extract_role(persona_description)
        
        # Determine skill level
        skill_level = self._determine_skill_level(persona_description)
        
        # Extract expertise domains
        expertise_domains = self._extract_expertise_domains(persona_description)
        
        # Extract focus areas
        focus_areas = self._extract_focus_areas(persona_description)
        
        # Generate relevant keywords
        keywords = self._generate_persona_keywords(persona_description, expertise_domains)
        
        return PersonaProfile(
            role=role,
            expertise_domains=expertise_domains,
            focus_areas=focus_areas,
            skill_level=skill_level,
            keywords=keywords
        )
    
    def analyze_job(self, job_description: str) -> JobRequirements:
        """
        Analyze job-to-be-done description.
        
        Args:
            job_description: Text description of the job/task
            
        Returns:
            JobRequirements object
        """
        logger.info(f"Analyzing job: {job_description}")
        
        # Extract primary goal
        primary_goal = self._extract_primary_goal(job_description)
        
        # Extract information needs
        information_needs = self._extract_information_needs(job_description)
        
        # Determine deliverable type
        deliverable_type = self._determine_deliverable_type(job_description)
        
        # Extract priority keywords
        priority_keywords = self._extract_priority_keywords(job_description)
        
        # Define success criteria
        success_criteria = self._define_success_criteria(job_description)
        
        return JobRequirements(
            primary_goal=primary_goal,
            information_needs=information_needs,
            deliverable_type=deliverable_type,
            priority_keywords=priority_keywords,
            success_criteria=success_criteria
        )
    
    def _extract_role(self, description: str) -> str:
        """Extract the primary role from persona description."""
        # Look for explicit role indicators
        role_patterns = [
            r'(PhD\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Researcher|Student|Analyst|Manager|Director)',
            r'(Undergraduate|Graduate)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Student',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(Analyst|Researcher|Scientist|Engineer|Manager)'
        ]
        
        for pattern in role_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        
        # Fallback to first meaningful phrase
        words = description.split()
        if len(words) >= 2:
            return ' '.join(words[:3])
        
        return description.strip()
    
    def _determine_skill_level(self, description: str) -> str:
        """Determine skill level from persona description."""
        description_lower = description.lower()
        
        for level, indicators in self.skill_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                return level
        
        return 'intermediate'  # Default
    
    def _extract_expertise_domains(self, description: str) -> List[str]:
        """Extract expertise domains from persona description."""
        domains = []
        description_lower = description.lower()
        
        for domain, keywords in self.domain_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                domains.append(domain)
        
        # Also look for explicit domain mentions
        domain_patterns = [
            r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:research|studies|field)',
        ]
        
        for pattern in domain_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                domains.append(match.lower().replace(' ', '_'))
        
        return list(set(domains))
    
    def _extract_focus_areas(self, description: str) -> List[str]:
        """Extract specific focus areas from persona description."""
        focus_areas = []
        
        # Look for "focusing on", "specializing in", etc.
        focus_patterns = [
            r'focus(?:ing|es)?\s+on\s+([^,.]+)',
            r'specializ(?:ing|es)?\s+in\s+([^,.]+)',
            r'expert(?:ise)?\s+in\s+([^,.]+)',
            r'working\s+(?:on|with)\s+([^,.]+)'
        ]
        
        for pattern in focus_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            focus_areas.extend([match.strip() for match in matches])
        
        return focus_areas
    
    def _generate_persona_keywords(self, description: str, domains: List[str]) -> Set[str]:
        """Generate relevant keywords for the persona."""
        keywords = set()
        
        # Add words from description
        words = re.findall(r'\b[a-zA-Z]{3,}\b', description.lower())
        keywords.update(words)
        
        # Add domain-specific keywords
        for domain in domains:
            if domain in self.domain_keywords:
                keywords.update(self.domain_keywords[domain])
        
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'its', 'said', 'each', 'make', 'most', 'over', 'such', 'very', 'what', 'with'}
        keywords = keywords - stop_words
        
        return keywords
    
    def _extract_primary_goal(self, job_description: str) -> str:
        """Extract the primary goal from job description."""
        # Look for action verbs at the beginning
        action_match = re.match(r'^([A-Z][a-z]+(?:\s+[a-z]+)*)', job_description)
        if action_match:
            return action_match.group(1)
        
        return job_description.split('.')[0].strip()
    
    def _extract_information_needs(self, job_description: str) -> List[str]:
        """Extract specific information needs from job description."""
        needs = []
        
        # Look for "focusing on", "including", etc.
        need_patterns = [
            r'focus(?:ing|es)?\s+on\s+([^,.]+)',
            r'includ(?:ing|es)?\s+([^,.]+)',
            r'such\s+as\s+([^,.]+)',
            r'(?:about|regarding|concerning)\s+([^,.]+)'
        ]
        
        for pattern in need_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            needs.extend([match.strip() for match in matches])
        
        return needs
    
    def _determine_deliverable_type(self, job_description: str) -> str:
        """Determine the type of deliverable expected."""
        description_lower = job_description.lower()
        
        for job_type, indicators in self.job_types.items():
            if any(indicator in description_lower for indicator in indicators):
                return job_type
        
        return 'analysis'  # Default
    
    def _extract_priority_keywords(self, job_description: str) -> Set[str]:
        """Extract priority keywords from job description."""
        keywords = set()
        
        # Extract all meaningful words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())
        keywords.update(words)
        
        # Remove common words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'its', 'said', 'each', 'make', 'most', 'over', 'such', 'very', 'what', 'with', 'given', 'that', 'this', 'should', 'will', 'from'}
        keywords = keywords - stop_words
        
        return keywords
    
    def _define_success_criteria(self, job_description: str) -> List[str]:
        """Define success criteria based on job description."""
        criteria = []
        
        # Extract explicit criteria
        if 'comprehensive' in job_description.lower():
            criteria.append('Comprehensive coverage of topic')
        
        if any(word in job_description.lower() for word in ['methodology', 'method']):
            criteria.append('Clear methodology explanation')
        
        if any(word in job_description.lower() for word in ['performance', 'benchmark', 'result']):
            criteria.append('Performance metrics and results')
        
        if any(word in job_description.lower() for word in ['trend', 'analysis', 'compare']):
            criteria.append('Trend analysis and comparisons')
        
        # Default criteria
        if not criteria:
            criteria = ['Relevant content extraction', 'Clear organization', 'Actionable insights']
        
        return criteria
