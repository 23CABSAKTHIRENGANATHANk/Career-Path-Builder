import os
import sys

# Add backend directory to path to allow importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from resume_analyzer import ResumeAnalyzer

def test_education_regex():
    analyzer = ResumeAnalyzer()
    
    test_text = """
    Education:
    Bachelor of Computer Application
    Bachelor in Computer
    Diploma in Computer Applications
    Diploma in Computer Applications - CSC
    helor of Computer in Application
    HSC
    """
    
    # Run the extraction
    edu_data = analyzer.extract_education(test_text)
    
    print("Extracted Degrees:")
    for deg in edu_data['degrees']:
        print(f" - {deg['degree']} (Field: {deg['field']})")

if __name__ == '__main__':
    test_education_regex()
