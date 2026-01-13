"""
Enhanced Flask Backend with Health Monitoring
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
import json
import time
from datetime import datetime

from resume_analyzer import ResumeAnalyzer
from career_engine import CareerEngine
from skill_analyzer import SkillAnalyzer
from roadmap_generator import RoadmapGenerator

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins including file://

# Initialize AI modules
resume_analyzer = ResumeAnalyzer()
career_engine = CareerEngine()
skill_analyzer = SkillAnalyzer()
roadmap_generator = RoadmapGenerator()

# Configure upload folder
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Server statistics
server_stats = {
    'start_time': datetime.now(),
    'requests_processed': 0,
    'resumes_analyzed': 0,
    'profiles_analyzed': 0
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint with server statistics"""
    uptime = datetime.now() - server_stats['start_time']
    return jsonify({
        'status': 'healthy',
        'message': 'AI Career Intelligence System is running',
        'uptime_seconds': int(uptime.total_seconds()),
        'statistics': {
            'requests_processed': server_stats['requests_processed'],
            'resumes_analyzed': server_stats['resumes_analyzed'],
            'profiles_analyzed': server_stats['profiles_analyzed']
        }
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'AI Career Intelligence System Backend',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'upload_resume': '/api/upload-resume',
            'analyze_profile': '/api/analyze-profile',
            'career_paths': '/api/career-paths',
            'skills': '/api/skills'
        }
    })

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload and analysis"""
    try:
        server_stats['requests_processed'] += 1
        
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'.pdf', '.docx', '.doc'}
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file format. Please upload PDF or DOCX'}), 400
        
        # Save file
        filename = f"resume_{os.urandom(8).hex()}{file_ext}"
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        # Analyze resume
        resume_data = resume_analyzer.analyze(file_path=str(filepath))
        
        # Clean up file after analysis
        os.remove(filepath)
        
        server_stats['resumes_analyzed'] += 1
        
        return jsonify({
            'success': True,
            'data': resume_data,
            'message': 'Resume analyzed successfully!'
        })
    
    except Exception as e:
        import traceback
        import logging
        logging.basicConfig(filename='error.log', level=logging.ERROR)
        logging.error(f"Error processing resume: {str(e)}\n{traceback.format_exc()}")
        print(f"❌ Error processing resume: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'details': traceback.format_exc()}), 500

@app.route('/api/analyze-profile', methods=['POST'])
def analyze_profile():
    """
    Comprehensive profile analysis
    Accepts user profile data and returns complete career analysis
    """
    try:
        server_stats['requests_processed'] += 1
        data = request.json
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate that at least some skills or interests are provided
        has_skills = (data.get('technical_skills') and len(data.get('technical_skills', [])) > 0) or \
                     (data.get('soft_skills') and len(data.get('soft_skills', [])) > 0)
        has_interests = data.get('interests') and len(data.get('interests', [])) > 0
        
        if not has_skills and not has_interests:
            return jsonify({'error': 'Please provide at least some skills or interests to analyze'}), 400
        
        # Build user profile
        user_profile = {
            'skills': {
                'technical': data.get('technical_skills', []),
                'soft': data.get('soft_skills', [])
            },
            'interests': data.get('interests', []),
            'education': {
                'degrees': data.get('degrees', []),
                'gpa': data.get('gpa')
            },
            'experience': data.get('experience', {}),
            'certifications': data.get('certifications', []),
            'learning_behavior': data.get('learning_behavior', {}),
            'city': data.get('city', 'Bangalore'), # Default to Bangalore
            'skill_ratings': data.get('skill_ratings', {})
        }
        
        # If resume data is provided, merge it
        if 'resume_data' in data:
            resume_data = data['resume_data']
            # Merge skills
            user_profile['skills']['technical'].extend(
                resume_data.get('skills', {}).get('technical', [])
            )
            user_profile['skills']['soft'].extend(
                resume_data.get('skills', {}).get('soft', [])
            )
            # Remove duplicates
            user_profile['skills']['technical'] = list(set(user_profile['skills']['technical']))
            user_profile['skills']['soft'] = list(set(user_profile['skills']['soft']))
            
            # Merge other data
            if resume_data.get('education'):
                user_profile['education'] = resume_data['education']
            if resume_data.get('experience'):
                user_profile['experience'] = resume_data['experience']
            if resume_data.get('certifications'):
                user_profile['certifications'] = resume_data['certifications']
            if resume_data.get('learning_behavior'):
                user_profile['learning_behavior'] = resume_data['learning_behavior']
        
        print(f"📊 Analyzing profile for user with {len(user_profile['skills']['technical'])} technical skills...")
        
        # Predict career path
        career_prediction = career_engine.predict_career_path(user_profile)
        
        # Analyze skill gaps
        skill_gap = skill_analyzer.analyze_skill_gap(
            user_profile['skills'],
            career_prediction['recommended_career']
        )
        
        # Compare with industry standards
        industry_comparison = skill_analyzer.compare_with_industry_standards(
            user_profile['skills'],
            career_prediction['recommended_career']
        )
        
        # Generate learning roadmap
        roadmap = roadmap_generator.generate_roadmap(
            career_prediction['recommended_career'],
            skill_gap,
            user_level=data.get('experience_level', 'beginner')
        )
        
        # Get quick wins
        quick_wins = roadmap_generator.get_quick_wins(skill_gap)
        
        # Compile complete response
        response = {
            'career_recommendation': {
                'career': career_prediction['recommended_career'],
                'description': career_prediction['description'],
                'confidence_score': career_prediction['confidence_score'],
                'reasoning': career_prediction['reasoning'],
                'job_roles': career_prediction['job_roles'],
                'companies': career_prediction['companies'],
                'salary_range': career_prediction['salary_range'],
                'growth_potential': career_prediction['growth_potential']
            },
            'skill_analysis': {
                'gap_analysis': skill_gap,
                'industry_comparison': industry_comparison,
                'quick_wins': quick_wins
            },
            'learning_roadmap': roadmap,
            'alternative_careers': career_prediction['alternative_paths']
        }
        
        server_stats['profiles_analyzed'] += 1
        print(f"✅ Profile analyzed successfully! Recommended career: {career_prediction['recommended_career']}")
        
        return jsonify({
            'success': True,
            'data': response,
            'message': 'Profile analyzed successfully!'
        })
    
    except Exception as e:
        import traceback
        print(f"❌ Error analyzing profile: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'details': traceback.format_exc()}), 500

@app.route('/api/career-paths', methods=['GET'])
def get_career_paths():
    """Get list of all available career paths"""
    try:
        server_stats['requests_processed'] += 1
        data_path = Path(__file__).parent / 'data' / 'career_data.json'
        with open(data_path, 'r') as f:
            career_data = json.load(f)
        
        careers = []
        for name, info in career_data['career_paths'].items():
            careers.append({
                'name': name,
                'description': info['description']
            })
        
        return jsonify({
            'success': True,
            'careers': careers
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get list of all available skills by category"""
    try:
        server_stats['requests_processed'] += 1
        data_path = Path(__file__).parent / 'data' / 'career_data.json'
        with open(data_path, 'r') as f:
            career_data = json.load(f)
        
        return jsonify({
            'success': True,
            'skills': career_data['skill_categories']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI Career Intelligence System Backend Starting...")
    print("=" * 60)
    print("📊 Modules loaded:")
    print("   ✓ Resume Analyzer")
    print("   ✓ Career Engine")
    print("   ✓ Skill Analyzer")
    print("   ✓ Roadmap Generator")
    print("=" * 60)
    print("🌐 Server running on http://localhost:5000")
    print("📝 API Documentation:")
    print("   • GET  /api/health          - Health check")
    print("   • POST /api/upload-resume   - Upload resume")
    print("   • POST /api/analyze-profile - Analyze profile")
    print("   • GET  /api/career-paths    - List careers")
    print("   • GET  /api/skills          - List skills")
    print("=" * 60)
    print("💡 Tip: Keep this terminal open while using the application")
    print("=" * 60)
    app.run(debug=True, port=5000)
