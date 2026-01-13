"""
Roadmap Generator Module
Creates personalized learning roadmaps based on skill gaps and career goals
"""

import json
from pathlib import Path

class RoadmapGenerator:
    def __init__(self):
        # Load career data
        data_path = Path(__file__).parent / 'data' / 'career_data.json'
        with open(data_path, 'r') as f:
            self.career_data = json.load(f)
    
    def generate_roadmap(self, career_path, skill_gap_analysis, user_level='beginner'):
        """
        Generate a personalized step-by-step learning roadmap
        Args:
            career_path: Target career path
            skill_gap_analysis: Output from SkillAnalyzer
            user_level: 'beginner', 'intermediate', or 'advanced'
        Returns:
            Structured learning roadmap with timeline
        """
        if career_path not in self.career_data['career_paths']:
            raise ValueError(f"Career path '{career_path}' not found")
        
        career_info = self.career_data['career_paths'][career_path]
        skills_analysis = skill_gap_analysis['skills_analysis']
        
        roadmap = {
            'career_path': career_path,
            'total_duration': '6-12 months',
            'phases': []
        }
        
        # Phase 1: Foundation (Critical Skills)
        if skills_analysis['missing_critical']:
            phase1 = self._create_foundation_phase(
                skills_analysis['missing_critical'],
                career_info,
                user_level
            )
            roadmap['phases'].append(phase1)
        
        # Phase 2: Core Competencies (Important Skills)
        if skills_analysis['missing_important']:
            phase2 = self._create_core_phase(
                skills_analysis['missing_important'],
                career_info,
                user_level
            )
            roadmap['phases'].append(phase2)
        
        # Phase 3: Specialization (Nice-to-have Skills)
        if skills_analysis['missing_nice_to_have']:
            phase3 = self._create_specialization_phase(
                skills_analysis['missing_nice_to_have'],
                career_info
            )
            roadmap['phases'].append(phase3)
        
        # Phase 4: Real-world Application
        phase4 = self._create_application_phase(career_info)
        roadmap['phases'].append(phase4)
        
        # Add official learning resources
        roadmap['recommended_resources'] = career_info.get('learning_resources', [])
        
        return roadmap
    
    def _create_foundation_phase(self, critical_skills, career_info, user_level):
        """Create Phase 1: Foundation building"""
        duration = '2-3 months' if user_level == 'beginner' else '1-2 months'
        
        steps = []
        for i, skill_data in enumerate(critical_skills[:3], 1):  # Top 3 critical skills
            skill = skill_data['skill']
            steps.append({
                'step': i,
                'title': f'Master {skill}',
                'description': f'Build strong foundation in {skill} through structured learning',
                'resources': self._get_skill_resources(skill, 'foundation'),
                'duration': '3-4 weeks',
                'deliverable': f'Complete 2-3 projects using {skill}'
            })
        
        return {
            'phase': 1,
            'title': 'Foundation Building',
            'description': 'Master the critical skills that form the backbone of this career',
            'duration': duration,
            'steps': steps,
            'milestone': 'Complete foundation projects and gain confidence in core skills'
        }
    
    def _create_core_phase(self, important_skills, career_info, user_level):
        """Create Phase 2: Core competencies"""
        duration = '2-3 months'
        
        steps = []
        for i, skill_data in enumerate(important_skills[:3], 1):
            skill = skill_data['skill']
            steps.append({
                'step': i,
                'title': f'Develop {skill} Skills',
                'description': f'Build practical expertise in {skill}',
                'resources': self._get_skill_resources(skill, 'intermediate'),
                'duration': '3-4 weeks',
                'deliverable': f'Build a real-world application using {skill}'
            })
        
        return {
            'phase': 2,
            'title': 'Core Competencies',
            'description': 'Develop important skills that make you job-ready',
            'duration': duration,
            'steps': steps,
            'milestone': 'Build a portfolio-worthy project combining multiple skills'
        }
    
    def _create_specialization_phase(self, nice_skills, career_info):
        """Create Phase 3: Specialization"""
        steps = []
        for i, skill_data in enumerate(nice_skills[:2], 1):
            skill = skill_data['skill']
            steps.append({
                'step': i,
                'title': f'Specialize in {skill}',
                'description': f'Gain competitive edge with {skill}',
                'resources': self._get_skill_resources(skill, 'advanced'),
                'duration': '2-3 weeks',
                'deliverable': f'Contribute to open source or build advanced feature using {skill}'
            })
        
        return {
            'phase': 3,
            'title': 'Specialization & Differentiation',
            'description': 'Stand out from other candidates with specialized skills',
            'duration': '1-2 months',
            'steps': steps,
            'milestone': 'Become proficient in a specialized area'
        }
    
    def _create_application_phase(self, career_info):
        """Create Phase 4: Real-world application"""
        steps = [
            {
                'step': 1,
                'title': 'Build Capstone Project',
                'description': 'Create a comprehensive project that showcases all your skills',
                'resources': ['GitHub for version control', 'Deploy on Vercel/Netlify/AWS'],
                'duration': '3-4 weeks',
                'deliverable': 'Fully functional, deployed application'
            },
            {
                'step': 2,
                'title': 'Create Professional Portfolio',
                'description': 'Build a portfolio website showcasing your projects',
                'resources': ['Portfolio templates', 'Personal branding guides'],
                'duration': '1 week',
                'deliverable': 'Live portfolio website'
            },
            {
                'step': 3,
                'title': 'Prepare for Interviews',
                'description': 'Practice technical interviews and coding challenges',
                'resources': ['LeetCode', 'HackerRank', 'Interview prep courses'],
                'duration': '2-3 weeks',
                'deliverable': 'Solve 50+ coding problems'
            },
            {
                'step': 4,
                'title': 'Start Applying',
                'description': 'Apply to entry-level positions and internships',
                'resources': ['LinkedIn', 'Indeed', 'Company career pages'],
                'duration': 'Ongoing',
                'deliverable': 'Land your first role!'
            }
        ]
        
        return {
            'phase': 4,
            'title': 'Real-World Application',
            'description': 'Apply your skills and land your first role',
            'duration': '2-3 months',
            'steps': steps,
            'milestone': 'Secure a job offer in your target career path'
        }
    
    def _get_skill_resources(self, skill, level):
        """Get learning resources for a specific skill"""
        # Simplified resource mapping
        resources_map = {
            'Python': ['Python.org tutorials', 'Automate the Boring Stuff', 'Real Python'],
            'JavaScript': ['JavaScript.info', 'Eloquent JavaScript', 'FreeCodeCamp'],
            'React': ['React official docs', 'React - The Complete Guide (Udemy)', 'Scrimba React'],
            'Node.js': ['Node.js docs', 'Node.js - The Complete Guide', 'NodeSchool'],
            'SQL': ['SQLBolt', 'Mode Analytics SQL Tutorial', 'Khan Academy SQL'],
            'Machine Learning': ['Coursera ML (Andrew Ng)', 'Fast.ai', 'Kaggle Learn'],
            'Docker': ['Docker official docs', 'Docker Mastery (Udemy)', 'Play with Docker'],
            'AWS': ['AWS Free Tier', 'A Cloud Guru', 'AWS Certified Solutions Architect'],
            'Git': ['Git official docs', 'GitHub Learning Lab', 'Atlassian Git tutorials'],
            'HTML': ['MDN Web Docs', 'FreeCodeCamp', 'W3Schools'],
            'CSS': ['CSS-Tricks', 'Flexbox Froggy', 'Grid Garden'],
            'Figma': ['Figma official tutorials', 'DesignCourse YouTube', 'Figma Community'],
        }
        
        return resources_map.get(skill, [f'{skill} official documentation', f'{skill} tutorials on YouTube', f'{skill} courses on Udemy'])
    
    def get_quick_wins(self, skill_gap_analysis):
        """Identify quick wins - easy skills to learn that boost confidence"""
        possessed = skill_gap_analysis['skills_analysis']['possessed']
        missing_nice = skill_gap_analysis['skills_analysis']['missing_nice_to_have']
        
        quick_wins = []
        
        # Skills that are easy to learn and complement existing skills
        if missing_nice:
            for skill_data in missing_nice[:2]:
                quick_wins.append({
                    'skill': skill_data['skill'],
                    'reason': 'Relatively easy to learn and complements your existing skills',
                    'estimated_time': '1-2 weeks',
                    'impact': 'Medium'
                })
        
        return quick_wins
