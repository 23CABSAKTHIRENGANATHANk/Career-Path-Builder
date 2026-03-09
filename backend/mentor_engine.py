import random

class MentorEngine:
    def __init__(self):
        self.context_responses = {
            "default": [
                "That's a great question! Based on your profile, I'd suggest focusing on building a strong portfolio.",
                "I see you're interested in {career}. A key next step would be to look into {skill} certifications.",
                "Growing in the {career} field requires consistent practice. Have you tried working on a hands-on project lately?",
                "Your current background and skills are a very strong match for {career}. Let's discuss how to land your first interview."
            ],
            "roadmap": [
                "The next step in your roadmap is crucial. Focus on mastering the basics before moving to advanced topics.",
                "I recommend spending at least 2 weeks on the current roadmap milestone.",
                "Don't rush! Building a deep understanding of {skill} will set you apart in interviews.",
                "I see you're focusing on the learning path for {career}. Remember to apply what you learn in real projects."
            ],
            "interview": [
                "When interviewing for {career}, emphasize your experience with {skill}.",
                "A common interview question for this role is 'Tell me about a complex problem you solved using {skill}'.",
                "Be ready to discuss your projects in detail. Recruiters love hearing about your thought process.",
                "For {career} interviews, highlighting your technical proficiency in {skill} will be key."
            ],
            "salary": [
                "The salary for {career} roles is quite competitive right now. Have you checked out the comparison chart in your dashboard?",
                "Expect a range based on your location. For {career}, experienced professionals can command significant premiums.",
                "Negotiating your first {career} salary is easier when you can demonstrate mastery of {skill}."
            ],
            "remote": [
                "Many {career} roles offer remote or hybrid options today. It's a great time to be in this field!",
                "If you're looking for remote work as a {career}, focus on building a strong online presence and GitHub portfolio.",
                "Building high proficiency in {skill} is a great way to unlock remote opportunities in {career}."
            ]
        }

    def get_response(self, message, context_data=None):
        """
        message: The user's input string
        context_data: Dictionary containing user profile/career info (usually the career_recommendation object)
        """
        message = message.lower()
        
        # 1. Determine the topic/intent based on keywords
        topic = "default"
        if any(word in message for word in ["roadmap", "learn", "study", "step", "path", "how to"]):
            topic = "roadmap"
        elif any(word in message for word in ["interview", "job", "hiring", "question", "apply", "recruiter", "interviewing"]):
            topic = "interview"
        elif any(word in message for word in ["salary", "pay", "money", "earn", "income"]):
            topic = "salary"
        elif any(word in message for word in ["remote", "wfh", "travel", "home", "location"]):
            topic = "remote"
        elif "hello" in message or "hi" in message or "hey" in message:
            # For greetings, pick a random welcoming response from default
            templates = [
                "Hello! How can I help you today on your journey to becoming a {career}?",
                "Hi there! Are you ready to dive deeper into your {career} roadmap?",
                "Hey! I'm here to support your growth in {career}. What's on your mind?"
            ]
            career = context_data.get('career', 'professional researcher') if context_data else "professional"
            return random.choice(templates).replace("{career}", career)
        
        # 2. Get response templates for this topic
        templates = self.context_responses.get(topic, self.context_responses["default"])
        response = random.choice(templates)
        
        # 3. Handle data extraction safely
        if not context_data:
            context_data = {}
            
        career = context_data.get('career', 'your chosen field')
        
        # Determine the most relevant skill/keyword to inject
        skill = "relevant technologies"
        
        # Priority 1: Check job_roles
        job_roles = context_data.get('job_roles', [])
        if job_roles and isinstance(job_roles, list):
            skill = job_roles[0]
        # Priority 2: Check skills if provided explicitly
        elif context_data.get('skills'):
            skills_input = context_data.get('skills')
            if isinstance(skills_input, list) and skills_input:
                skill = skills_input[0]
            elif isinstance(skills_input, dict):
                tech = skills_input.get('technical', [])
                if tech:
                    skill = tech[0]
        
        # 4. Format and return
        response = response.replace("{career}", career).replace("{skill}", str(skill))
        return response

    def generate_mentor_advice(self, user_data):
        """Generate a proactive piece of advice based on user analysis"""
        if not user_data:
            return "Hello! I'm your AI Mentor. Let's start by analyzing your profile to give you personalized advice."

        # user_data is the full response object from /api/analyze-profile
        career_rec = user_data.get('career_recommendation', {})
        career = career_rec.get('career', 'a professional career')
        
        # Try to get missing skills from gap analysis
        skill_analysis = user_data.get('skill_analysis', {})
        gap_analysis = skill_analysis.get('gap_analysis', {})
        missing_skills = gap_analysis.get('missing_critical_skills', [])
        
        if missing_skills and len(missing_skills) > 0:
            top_skill = missing_skills[0]
            # Handle both string and list/dict formats safely
            skill_name = top_skill if isinstance(top_skill, str) else str(top_skill)
            return f"Hi! I'm your AI Mentor. I noticed you're aiming for **{career}**. A great first step would be to start learning **{skill_name}** today!"
        
        return f"Welcome! As your AI Mentor, I'm here to help you navigate your journey toward becoming a top-tier **{career}**."
