"""
Resume Analyzer Module
Extracts skills, projects, experience, and education from resume text using NLP
"""

import re
import json
from pathlib import Path
import PyPDF2
import docx

class ResumeAnalyzer:
    def __init__(self):
        # Load career data for skill matching
        data_path = Path(__file__).parent / 'data' / 'career_data.json'
        with open(data_path, 'r') as f:
            self.career_data = json.load(f)
        
        # Build comprehensive skill list from all career paths
        self.all_skills = set()
        for career in self.career_data['career_paths'].values():
            self.all_skills.update(career['required_skills']['technical'])
            self.all_skills.update(career['required_skills']['soft'])
        
        # Add skills from categories
        for category_skills in self.career_data['skill_categories'].values():
            self.all_skills.update(category_skills)
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX: {e}")
        return text
    
    def extract_text(self, file_path):
        """Extract text from resume file (PDF or DOCX)"""
        file_path = Path(file_path)
        if file_path.suffix.lower() == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or DOCX.")
    
    def extract_skills(self, text):
        """Extract technical and soft skills from resume text"""
        text_lower = text.lower()
        found_skills = {
            'technical': [],
            'soft': []
        }
        
        # Match skills (case-insensitive)
        for skill in self.all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                # Categorize skill
                is_soft_skill = skill in self.career_data['skill_categories']['soft_skills']
                if is_soft_skill:
                    found_skills['soft'].append(skill)
                else:
                    found_skills['technical'].append(skill)
        
        return found_skills
    
    def extract_education(self, text):
        """Extract education details from resume"""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'(Bachelor|B\.?S\.?|B\.?A\.?|B\.?Tech|B\.?E\.?)\s+(?:of\s+)?(?:Science\s+)?(?:in\s+)?([A-Za-z\s]+)',
            r'(Master|M\.?S\.?|M\.?A\.?|M\.?Tech|M\.?E\.?)\s+(?:of\s+)?(?:Science\s+)?(?:in\s+)?([A-Za-z\s]+)',
            r'(Ph\.?D\.?|Doctorate)\s+(?:in\s+)?([A-Za-z\s]+)',
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                education.append({
                    'degree': match.group(1),
                    'field': match.group(2).strip()
                })
        
        # Extract GPA/marks if present
        gpa_pattern = r'(?:GPA|CGPA)[\s:]+(\d+\.?\d*)'
        gpa_matches = re.findall(gpa_pattern, text, re.IGNORECASE)
        
        return {
            'degrees': education,
            'gpa': gpa_matches[0] if gpa_matches else None
        }
    
    def extract_projects(self, text):
        """Extract project information from resume"""
        projects = []
        
        # Look for project sections
        project_section_pattern = r'(?:projects?|portfolio)[\s:]+(.+?)(?=\n\n|\n[A-Z]|$)'
        matches = re.finditer(project_section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            project_text = match.group(1)
            # Split by bullet points or newlines
            project_items = re.split(r'\n[\•\-\*]|\n', project_text)
            for item in project_items:
                item = item.strip()
                if len(item) > 20:  # Filter out very short items
                    projects.append(item[:200])  # Limit length
        
        return projects[:5]  # Return top 5 projects
    
    def extract_experience(self, text):
        """Extract work experience from resume"""
        experience = []
        
        # Look for experience sections
        exp_section_pattern = r'(?:experience|employment|work history)[\s:]+(.+?)(?=\n\n|\neducation|\nprojects?|$)'
        matches = re.finditer(exp_section_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            exp_text = match.group(1)
            # Extract job titles and companies
            job_pattern = r'([A-Z][A-Za-z\s]+(?:Engineer|Developer|Designer|Analyst|Manager))'
            jobs = re.findall(job_pattern, exp_text)
            experience.extend(jobs[:3])  # Top 3 positions
        
        # Calculate years of experience (rough estimate)
        year_pattern = r'\b(20\d{2})\b'
        years = re.findall(year_pattern, text)
        years_of_exp = 0
        if len(years) >= 2:
            years_sorted = sorted([int(y) for y in years])
            years_of_exp = years_sorted[-1] - years_sorted[0]
        
        return {
            'positions': experience,
            'years': years_of_exp
        }
    
    def extract_certifications(self, text):
        """Extract certifications from resume"""
        certifications = []
        
        # Common certification patterns
        cert_keywords = ['certified', 'certification', 'certificate', 'AWS', 'Google', 'Microsoft', 'CompTIA']
        
        for keyword in cert_keywords:
            pattern = r'([A-Z][A-Za-z\s]+' + re.escape(keyword) + r'[A-Za-z\s\+]*)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend([m.strip() for m in matches])
        
        return list(set(certifications))[:5]  # Unique, top 5
    
    def analyze_learning_behavior(self, resume_data):
        """Analyze learning patterns from resume data"""
        behavior = {
            'self_learner': False,
            'project_oriented': False,
            'certification_focused': False,
            'academic_focused': False
        }
        
        # Check for self-learning indicators
        if len(resume_data['projects']) > 2:
            behavior['project_oriented'] = True
            behavior['self_learner'] = True
        
        # Check for certifications
        if len(resume_data['certifications']) > 1:
            behavior['certification_focused'] = True
            behavior['self_learner'] = True
        
        # Check academic focus
        if resume_data['education']['degrees']:
            behavior['academic_focused'] = True
        
        return behavior
    
    def analyze(self, file_path=None, text=None):
        """
        Main analysis function
        Args:
            file_path: Path to resume file (PDF or DOCX)
            text: Resume text (if file_path not provided)
        Returns:
            Dictionary with extracted information
        """
        if file_path:
            text = self.extract_text(file_path)
        elif not text:
            raise ValueError("Either file_path or text must be provided")
        
        # Extract all components
        skills = self.extract_skills(text)
        education = self.extract_education(text)
        projects = self.extract_projects(text)
        experience = self.extract_experience(text)
        certifications = self.extract_certifications(text)
        
        resume_data = {
            'skills': skills,
            'education': education,
            'projects': projects,
            'experience': experience,
            'certifications': certifications,
            'raw_text': text[:500]  # First 500 chars for reference
        }
        
        # Analyze learning behavior
        resume_data['learning_behavior'] = self.analyze_learning_behavior(resume_data)
        
        return resume_data
