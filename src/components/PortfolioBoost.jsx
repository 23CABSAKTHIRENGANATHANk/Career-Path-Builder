import { useState, useEffect } from 'react';
import './PortfolioBoost.css';

function PortfolioBoost({ career }) {
    const [startedProjects, setStartedProjects] = useState(() => {
        try {
            const saved = localStorage.getItem('careerStartedProjects');
            return saved ? JSON.parse(saved) : {};
        } catch (e) {
            return {};
        }
    });

    const [startingId, setStartingId] = useState(null);

    useEffect(() => {
        localStorage.setItem('careerStartedProjects', JSON.stringify(startedProjects));
    }, [startedProjects]);

    const handleStart = (projectId) => {
        setStartingId(projectId);
        setTimeout(() => {
            setStartedProjects(prev => ({
                ...prev,
                [projectId]: true
            }));
            setStartingId(null);

            // Redirect to the GitHub link if they want
            // window.open("https://github.com/topics/starter-project", "_blank");
        }, 1200);
    };

    const projects = [
        {
            title: "Phase 1: Foundation Project",
            name: "The Core Builder",
            description: `Build a robust foundation for your ${career} career by implementing the essential building blocks.`,
            difficulty: "Beginner",
            tasks: ["Set up development environment", "Implement core logic", "Write unit tests"],
            link: "https://github.com/topics/starter-project"
        },
        {
            title: "Phase 2: Intermediate Challenge",
            name: "The Advanced Integrator",
            description: `Connect multiple systems and demonstrate your ability to handle complex data flows as a ${career}.`,
            difficulty: "Intermediate",
            tasks: ["API Integration", "State Management", "User Authentication"],
            link: "https://github.com/topics/fullstack-app"
        },
        {
            title: "Phase 3: Portfolio Masterpiece",
            name: "Industry Elite Solution",
            description: `A production-ready project that showcases your readiness for a Senior ${career} role.`,
            difficulty: "Advanced",
            tasks: ["Performance Optimization", "Scalability Planning", "CI/CD Pipeline"],
            link: "https://github.com/topics/industry-projects"
        }
    ];

    return (
        <div className="portfolio-boost-container fade-in">
            <div className="pb-header">
                <h3>🏗️ Portfolio Builder & Projects</h3>
                <p>Build these projects to showcase your skills as a <strong>{career}</strong>.</p>
            </div>

            <div className="pb-grid">
                {projects.map((project, index) => (
                    <div key={index} className="pb-card glass-card">
                        <div className="pb-phase-badge">{project.title}</div>
                        <h4>{project.name}</h4>
                        <p className="pb-description">{project.description}</p>

                        <div className="pb-tasks">
                            <h5>Key Deliverables:</h5>
                            <ul>
                                {project.tasks.map((task, tIndex) => (
                                    <li key={tIndex}>✓ {task}</li>
                                ))}
                            </ul>
                        </div>

                        <div className="pb-footer">
                            <span className={`difficulty-badge ${project.difficulty.toLowerCase()}`}>
                                {project.difficulty}
                            </span>
                            <button
                                className={`pb-view-link-btn ${startedProjects[index] ? 'started' : ''}`}
                                onClick={() => handleStart(index)}
                                disabled={startedProjects[index] || startingId === index}
                                style={{
                                    padding: '8px 16px',
                                    border: 'none',
                                    borderRadius: '8px',
                                    background: startedProjects[index] ? 'linear-gradient(135deg, #10B981 0%, #059669 100%)' : 'var(--primary-gradient)',
                                    color: 'white',
                                    fontWeight: '600',
                                    cursor: startedProjects[index] ? 'default' : 'pointer'
                                }}
                            >
                                {startingId === index ? 'Initializing...' :
                                    startedProjects[index] ? 'Project Started ✓' : 'Start Project ↗'}
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default PortfolioBoost;
