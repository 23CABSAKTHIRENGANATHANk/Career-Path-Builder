"""
Skill Analyzer Module
Analyzes skill gaps between user profile and career requirements
"""

import json
from pathlib import Path

class SkillAnalyzer:
    def __init__(self):
        # Load career data
        data_path = Path(__file__).parent / 'data' / 'career_data.json'
        with open(data_path, 'r') as f:
            self.career_data = json.load(f)
    
    def analyze_skill_gap(self, user_skills, career_path):
        """
        Analyze skill gaps for a specific career path
        Returns detailed gap analysis with priorities
        """
        if career_path not in self.career_data['career_paths']:
            raise ValueError(f"Career path '{career_path}' not found")
        
        career_info = self.career_data['career_paths'][career_path]
        required_skills = career_info['required_skills']
        skill_weights = career_info['skill_weights']
        
        # Combine user skills (normalize to lowercase)
        all_user_skills = [s.lower() for s in (
            user_skills.get('technical', []) +
            user_skills.get('soft', [])
        )]
        
        # Categorize skills
        skills_analysis = {
            'possessed': [],
            'missing_critical': [],
            'missing_important': [],
            'missing_nice_to_have': []
        }
        
        # Analyze each required skill
        for skill, weight in skill_weights.items():
            if skill.lower() in all_user_skills:
                skills_analysis['possessed'].append({
                    'skill': skill,
                    'weight': weight,
                    'proficiency': 'Known'  # Could be enhanced with proficiency levels
                })
            else:
                # Categorize by priority based on weight
                skill_data = {
                    'skill': skill,
                    'weight': weight
                }
                
                if weight >= 9:
                    skills_analysis['missing_critical'].append(skill_data)
                elif weight >= 7:
                    skills_analysis['missing_important'].append(skill_data)
                else:
                    skills_analysis['missing_nice_to_have'].append(skill_data)
        
        # Calculate gap metrics
        total_skills = len(skill_weights)
        possessed_count = len(skills_analysis['possessed'])
        gap_percentage = ((total_skills - possessed_count) / total_skills) * 100
        
        # Calculate readiness score (weighted)
        total_weight = sum(skill_weights.values())
        possessed_weight = sum(s['weight'] for s in skills_analysis['possessed'])
        readiness_score = (possessed_weight / total_weight) * 100
        
        return {
            'career_path': career_path,
            'skills_analysis': skills_analysis,
            'metrics': {
                'total_required_skills': total_skills,
                'possessed_skills': possessed_count,
                'missing_skills': total_skills - possessed_count,
                'gap_percentage': round(gap_percentage, 2),
                'readiness_score': round(readiness_score, 2)
            },
            'recommendations': self._generate_recommendations(skills_analysis)
        }
    
    def _generate_recommendations(self, skills_analysis):
        """Generate actionable recommendations based on skill gaps"""
        recommendations = []
        
        # Critical skills recommendation
        if skills_analysis['missing_critical']:
            critical_skills = [s['skill'] for s in skills_analysis['missing_critical']]
            recommendations.append({
                'priority': 'HIGH',
                'title': 'Master Critical Skills First',
                'description': f"Focus immediately on learning {', '.join(critical_skills[:3])}. These are essential for this career path.",
                'timeline': '1-3 months'
            })
        
        # Important skills recommendation
        if skills_analysis['missing_important']:
            important_skills = [s['skill'] for s in skills_analysis['missing_important']]
            recommendations.append({
                'priority': 'MEDIUM',
                'title': 'Build Important Competencies',
                'description': f"After mastering the basics, develop skills in {', '.join(important_skills[:3])} to become more competitive.",
                'timeline': '3-6 months'
            })
        
        # Nice-to-have skills recommendation
        if skills_analysis['missing_nice_to_have']:
            nice_skills = [s['skill'] for s in skills_analysis['missing_nice_to_have']]
            recommendations.append({
                'priority': 'LOW',
                'title': 'Expand Your Toolkit',
                'description': f"Once you're comfortable with core skills, consider learning {', '.join(nice_skills[:2])} to stand out.",
                'timeline': '6+ months'
            })
        
        # Leverage existing skills
        if skills_analysis['possessed']:
            possessed_skills = [s['skill'] for s in skills_analysis['possessed'][:3]]
            recommendations.append({
                'priority': 'INFO',
                'title': 'Leverage Your Strengths',
                'description': f"You already have {', '.join(possessed_skills)}. Build projects that showcase these skills while learning new ones.",
                'timeline': 'Ongoing'
            })
        
        return recommendations
    
    def compare_with_industry_standards(self, user_skills, career_path):
        """
        Compare user's skill set with industry standards
        Returns benchmark comparison
        """
        gap_analysis = self.analyze_skill_gap(user_skills, career_path)
        
        # Industry benchmarks (simplified)
        benchmarks = {
            'entry_level': 40,    # 40% skill match
            'mid_level': 70,      # 70% skill match
            'senior_level': 90    # 90% skill match
        }
        
        readiness = gap_analysis['metrics']['readiness_score']
        
        # Determine level
        if readiness >= benchmarks['senior_level']:
            level = 'Senior Level'
            message = 'You meet senior-level requirements! You\'re ready for advanced roles.'
        elif readiness >= benchmarks['mid_level']:
            level = 'Mid Level'
            message = 'You meet mid-level requirements. Focus on advanced skills to reach senior level.'
        elif readiness >= benchmarks['entry_level']:
            level = 'Entry Level'
            message = 'You meet entry-level requirements. Keep learning to advance to mid-level.'
        else:
            level = 'Learning Phase'
            message = 'You\'re in the learning phase. Focus on building foundational skills.'
        
        return {
            'current_level': level,
            'readiness_score': readiness,
            'benchmarks': benchmarks,
            'message': message,
            'next_milestone': self._get_next_milestone(readiness, benchmarks)
        }
    
    def _get_next_milestone(self, current_score, benchmarks):
        """Determine next milestone for the user"""
        if current_score < benchmarks['entry_level']:
            gap = benchmarks['entry_level'] - current_score
            return {
                'target': 'Entry Level',
                'score_needed': benchmarks['entry_level'],
                'gap': round(gap, 2),
                'message': f'You need {gap:.0f}% more skill coverage to reach entry level.'
            }
        elif current_score < benchmarks['mid_level']:
            gap = benchmarks['mid_level'] - current_score
            return {
                'target': 'Mid Level',
                'score_needed': benchmarks['mid_level'],
                'gap': round(gap, 2),
                'message': f'You need {gap:.0f}% more skill coverage to reach mid level.'
            }
        elif current_score < benchmarks['senior_level']:
            gap = benchmarks['senior_level'] - current_score
            return {
                'target': 'Senior Level',
                'score_needed': benchmarks['senior_level'],
                'gap': round(gap, 2),
                'message': f'You need {gap:.0f}% more skill coverage to reach senior level.'
            }
        else:
            return {
                'target': 'Expert Level',
                'score_needed': 100,
                'gap': 0,
                'message': 'You\'ve mastered the core skills! Focus on specialization and leadership.'
            }
