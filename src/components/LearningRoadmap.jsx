import { useState, useEffect } from 'react';
import './LearningRoadmap.css';

function LearningRoadmap({ data }) {
    const { phases, total_duration, recommended_resources } = data;

    // Gamification State
    const [completedSteps, setCompletedSteps] = useState(() => {
        try {
            const savedProgress = localStorage.getItem('careerRoadmapProgress');
            return savedProgress ? JSON.parse(savedProgress) : {};
        } catch (e) {
            return {};
        }
    });

    useEffect(() => {
        localStorage.setItem('careerRoadmapProgress', JSON.stringify(completedSteps));
    }, [completedSteps]);

    const toggleStep = (phaseIndex, stepIndex) => {
        const key = `${phaseIndex}-${stepIndex}`;
        setCompletedSteps(prev => ({
            ...prev,
            [key]: !prev[key]
        }));
    };

    // Calculate XP
    const totalSteps = phases.reduce((acc, phase) => acc + phase.steps.length, 0);
    const completedCount = Object.values(completedSteps).filter(Boolean).length;
    const progressPercent = totalSteps > 0 ? (completedCount / totalSteps) * 100 : 0;
    const xp = completedCount * 100;
    const level = Math.floor(xp / 500) + 1;
    const xpToNextLevel = 500 - (xp % 500);

    return (
        <div className="lr-roadmap-container">
            {/* Gamification Dashboard */}
            <div className="lr-gamification-bar glass-card-glow">
                <div className="lr-xp-info">
                    <div className="lr-level-badge">LVL {level}</div>
                    <div className="lr-xp-text">
                        <span>Career XP: <strong>{xp}</strong></span>
                        <span className="lr-xp-next">{xpToNextLevel} XP to next level</span>
                    </div>
                </div>
                <div className="lr-overall-progress">
                    <div className="lr-progress-track">
                        <div className="lr-progress-fill" style={{ width: `${progressPercent}%` }}></div>
                    </div>
                    <span className="lr-progress-percent">{Math.round(progressPercent)}% Journey Complete</span>
                </div>
            </div>

            {progressPercent === 100 && (
                <div className="lr-completion-banner glass-card-glow animate-bounce-subtle">
                    <span className="celebration-icon">🎊</span>
                    <div className="celebration-text">
                        <h3>Congratulations! You've Mastered Your Roadmap!</h3>
                        <p>You are now an <strong>Industry Elite (Level {level})</strong>. You're ready for your dream career!</p>
                    </div>
                </div>
            )}

            <div className="roadmap-header glass-card">
                <h2>Your Personalized Learning Roadmap</h2>
                <p>Estimated Duration: <span className="duration-badge">{total_duration}</span></p>
            </div>

            {/* Timeline */}
            <div className="lr-timeline">
                {phases.map((phase, index) => (
                    <div key={index} className="lr-timeline-item">
                        <div className="lr-timeline-marker">
                            <div className="lr-marker-dot">{phase.phase}</div>
                            <div className="lr-marker-line"></div>
                        </div>

                        <div className="lr-timeline-content glass-card">
                            <div className="lr-phase-header">
                                <h3>{phase.title}</h3>
                                <span className="lr-phase-duration badge badge-primary">{phase.duration}</span>
                            </div>

                            <p className="lr-phase-description">{phase.description}</p>

                            <div className="lr-phase-steps">
                                {phase.steps.map((step, stepIndex) => {
                                    const isCompleted = completedSteps[`${index}-${stepIndex}`];
                                    return (
                                        <div
                                            key={stepIndex}
                                            className={`lr-step-card ${isCompleted ? 'completed' : ''}`}
                                            onClick={() => toggleStep(index, stepIndex)}
                                        >
                                            <div className="lr-step-header">
                                                <div className="lr-step-checkbox">
                                                    {isCompleted ? '✅' : '○'}
                                                </div>
                                                <div className="lr-step-number">Step {step.step}</div>
                                                <h4>{step.title}</h4>
                                            </div>

                                            <p className="lr-step-description">{step.description}</p>

                                            <div className="lr-step-meta">
                                                <span className="lr-step-duration">⏱ {step.duration}</span>
                                                <span className="lr-step-deliverable">🎯 {step.deliverable}</span>
                                            </div>

                                            {step.resources && step.resources.length > 0 && (
                                                <div className="lr-step-resources">
                                                    <strong>Resources:</strong>
                                                    <ul>
                                                        {step.resources.map((resource, resIndex) => (
                                                            <li key={resIndex}>{resource}</li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            )}
                                            {isCompleted && <div className="lr-step-badge">MASTERED +100 XP</div>}
                                        </div>
                                    );
                                })}
                            </div>

                            <div className="lr-phase-milestone">
                                <span className="lr-milestone-icon">🏆</span>
                                <span className="lr-milestone-text">Milestone: {phase.milestone}</span>
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
