// Test data for development/debugging
// You can paste this in browser console to test the report page

const testReportData = {
    career_recommendation: {
        career: "Full-Stack Developer",
        description: "A full-stack developer combines frontend and backend expertise to build complete web applications. This path leverages your strong technical foundation and problem-solving skills.",
        confidence_score: 92,
        salary_range: "$120,000 - $180,000",
        growth_potential: "High",
        reasoning: "Based on your JavaScript, React, Python, and database knowledge, you're well-suited for full-stack development. Your problem-solving skills and quick learning ability make this an excellent career path.",
        companies: [
            "Google",
            "Microsoft",
            "Amazon",
            "Apple",
            "Meta",
            "Netflix",
            "Uber",
            "Airbnb"
        ]
    },
    skill_analysis: {
        gap_analysis: {
            strong_matches: [
                "JavaScript",
                "React",
                "Python",
                "SQL",
                "Git",
                "Problem Solving",
                "API Design",
                "Database Design"
            ],
            missing_critical_skills: [
                "DevOps & Docker",
                "Kubernetes",
                "System Design",
                "Cloud Architecture",
                "Microservices",
                "Advanced Caching"
            ]
        }
    },
    learning_roadmap: {
        phases: [
            {
                phase: 1,
                title: "Advanced Backend Fundamentals",
                duration: "3 months",
                topics: [
                    "Advanced Node.js and async patterns",
                    "RESTful API Design and Best Practices",
                    "Database Optimization and Indexing",
                    "Authentication and Security",
                    "Error Handling and Logging"
                ]
            },
            {
                phase: 2,
                title: "DevOps and Cloud Technologies",
                duration: "4 months",
                topics: [
                    "Docker Containerization",
                    "Kubernetes Orchestration",
                    "CI/CD Pipelines",
                    "AWS or GCP Fundamentals",
                    "Infrastructure as Code"
                ]
            },
            {
                phase: 3,
                title: "System Design and Architecture",
                duration: "4 months",
                topics: [
                    "Scalable System Design",
                    "Distributed Systems",
                    "Load Balancing and Caching",
                    "Microservices Architecture",
                    "Database Scaling Strategies"
                ]
            }
        ]
    },
    alternative_careers: [
        {
            career: "Backend Engineer",
            match_percentage: 88
        },
        {
            career: "DevOps Engineer",
            match_percentage: 85
        },
        {
            career: "Solutions Architect",
            match_percentage: 82
        }
    ]
};

// To use this test data:
// 1. Open browser console (F12)
// 2. Paste the above code
// 3. Then paste this:
localStorage.setItem('careerAnalysisData', JSON.stringify(testReportData));
window.location.href = '/report';
