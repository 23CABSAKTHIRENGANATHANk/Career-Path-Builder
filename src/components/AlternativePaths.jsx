import { useState } from 'react';
import './AlternativePaths.css';

function AlternativePaths({ data }) {
    const [selectedCareer, setSelectedCareer] = useState(null);

    const handleExplore = (alternative) => {
        setSelectedCareer(alternative);
    };

    const closeModal = () => {
        setSelectedCareer(null);
    };

    return (
        <div className="alternatives-container">
            <div className="alternatives-header">
                <h2>Alternative Career Paths</h2>
                <p>Explore other careers that match your profile</p>
            </div>

            <div className="alternatives-grid">
                {data.map((alternative, index) => (
                    <div key={index} className="alternative-card glass-card">
                        <div className="alternative-header">
                            <h3>{alternative.career}</h3>
                            <div className="match-score">
                                <div className="score-circle-small">
                                    <svg viewBox="0 0 36 36">
                                        <circle cx="18" cy="18" r="16" className="score-bg-small" />
                                        <circle
                                            cx="18"
                                            cy="18"
                                            r="16"
                                            className="score-fill-small"
                                            style={{
                                                strokeDasharray: `${alternative.match_score} 100`
                                            }}
                                        />
                                    </svg>
                                    <span className="score-text-small">{Math.round(alternative.match_score)}%</span>
                                </div>
                            </div>
                        </div>

                        <p className="alternative-description">{alternative.description}</p>

                        <div className="alternative-reason">
                            <strong>Why this path?</strong>
                            <p>{alternative.why}</p>
                        </div>

                        <button
                            className="btn btn-secondary explore-btn"
                            onClick={() => handleExplore(alternative)}
                        >
                            Explore This Path →
                        </button>
                    </div>
                ))}
            </div>

            <div className="glass-card comparison-tip">
                <h3>💡 Not Sure Which Path to Choose?</h3>
                <p>
                    Consider trying small projects or courses in each area to see what resonates with you.
                    Your interests and strengths may evolve as you learn more. The best career path is one
                    that aligns with both your skills and your passion.
                </p>
            </div>

            {/* Career Details Modal */}
            {selectedCareer && (
                <div className="modal-overlay" onClick={closeModal}>
                    <div className="modal-content glass-card" onClick={(e) => e.stopPropagation()}>
                        <button className="modal-close" onClick={closeModal}>✕</button>

                        <div className="modal-header">
                            <h2>🎯 {selectedCareer.career}</h2>
                            <div className="modal-score">
                                <span className="score-badge">{Math.round(selectedCareer.match_score)}% Match</span>
                            </div>
                        </div>

                        <div className="modal-body">
                            <div className="modal-section">
                                <h3>📋 Overview</h3>
                                <p>{selectedCareer.description}</p>
                            </div>

                            <div className="modal-section">
                                <h3>💡 Why This Path?</h3>
                                <p>{selectedCareer.why}</p>
                            </div>

                            <div className="modal-section">
                                <h3>🚀 Next Steps</h3>
                                <ul>
                                    <li>Research job postings in this field</li>
                                    <li>Take online courses to build relevant skills</li>
                                    <li>Connect with professionals in this career</li>
                                    <li>Start small projects to gain experience</li>
                                </ul>
                            </div>

                            <div className="modal-note">
                                <strong>💡 Pro Tip:</strong> Start with small projects or courses to test if this path resonates with you before fully committing.
                            </div>
                        </div>

                        <div className="modal-footer">
                            <button className="btn btn-primary" onClick={closeModal}>
                                Got it! ✓
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default AlternativePaths;
