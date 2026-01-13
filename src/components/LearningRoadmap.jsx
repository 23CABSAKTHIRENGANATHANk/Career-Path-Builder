import './LearningRoadmap.css';

function LearningRoadmap({ data }) {
    const { phases, total_duration, recommended_resources } = data;

    return (
        <div className="roadmap-container">
            <div className="roadmap-header glass-card">
                <h2>Your Personalized Learning Roadmap</h2>
                <p>Estimated Duration: <span className="duration-badge">{total_duration}</span></p>
            </div>

            {/* Timeline */}
            <div className="timeline">
                {phases.map((phase, index) => (
                    <div key={index} className="timeline-item">
                        <div className="timeline-marker">
                            <div className="marker-dot">{phase.phase}</div>
                            <div className="marker-line"></div>
                        </div>

                        <div className="timeline-content glass-card">
                            <div className="phase-header">
                                <h3>{phase.title}</h3>
                                <span className="phase-duration badge badge-primary">{phase.duration}</span>
                            </div>

                            <p className="phase-description">{phase.description}</p>

                            <div className="phase-steps">
                                {phase.steps.map((step, stepIndex) => (
                                    <div key={stepIndex} className="step-card">
                                        <div className="step-header">
                                            <div className="step-number">Step {step.step}</div>
                                            <h4>{step.title}</h4>
                                        </div>

                                        <p className="step-description">{step.description}</p>

                                        <div className="step-meta">
                                            <span className="step-duration">⏱ {step.duration}</span>
                                            <span className="step-deliverable">🎯 {step.deliverable}</span>
                                        </div>

                                        {step.resources && step.resources.length > 0 && (
                                            <div className="step-resources">
                                                <strong>Resources:</strong>
                                                <ul>
                                                    {step.resources.map((resource, resIndex) => (
                                                        <li key={resIndex}>{resource}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>

                            <div className="phase-milestone">
                                <span className="milestone-icon">🏆</span>
                                <span className="milestone-text">Milestone: {phase.milestone}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Recommended Resources */}
            {recommended_resources && recommended_resources.length > 0 && (
                <div className="glass-card resources-section">
                    <h3>📚 Recommended Learning Resources</h3>
                    <div className="resources-grid">
                        {recommended_resources.map((resource, index) => (
                            <div key={index} className="resource-card">
                                <div className="resource-type badge badge-success">
                                    {resource.type}
                                </div>
                                <h4>{resource.name}</h4>
                                <p className="resource-platform">{resource.platform}</p>
                                <p className="resource-duration">Duration: {resource.duration}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default LearningRoadmap;
