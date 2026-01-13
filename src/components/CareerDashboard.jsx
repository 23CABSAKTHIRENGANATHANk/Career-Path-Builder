import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SkillGapChart from './SkillGapChart';
import LearningRoadmap from './LearningRoadmap';
import AlternativePaths from './AlternativePaths';
import SalaryComparisonChart from './SalaryComparisonChart';
import './CareerDashboard.css';
import './EnhancedUI.css';
import './VibrantColors.css';
import './Enhanced3D.css';
import './BackButton.css';

function CareerDashboard({ data, onReset }) {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('overview');

    // Validate data exists and has required fields
    if (!data) {
        return (
            <div className="no-data-state">
                <div className="error-card">
                    <h2>No Data Found</h2>
                    <p>Please create a new analysis to view the dashboard.</p>
                    <button onClick={() => navigate('/')}>
                        Create New Analysis
                    </button>
                </div>
            </div>
        );
    }

    const { career_recommendation, skill_analysis, learning_roadmap, alternative_careers } = data;

    // Convert USD salary to INR (1 USD = 83 INR approx)
    const convertToINR = (salaryRange) => {
        if (!salaryRange) return 'Not specified';

        try {
            // Remove $ and commas, then extract all numbers
            const cleaned = salaryRange.replace(/\$/g, '').replace(/,/g, '');
            const numbers = cleaned.match(/\d+/g);

            if (!numbers || numbers.length < 2) {
                console.log('Could not parse salary:', salaryRange);
                return salaryRange;
            }

            const min = parseInt(numbers[0]);
            const max = parseInt(numbers[1]);

            if (isNaN(min) || isNaN(max)) {
                console.log('Invalid numbers:', min, max);
                return salaryRange;
            }

            // Convert to INR (1 USD ≈ 83 INR)
            const minINR = Math.round(min * 83);
            const maxINR = Math.round(max * 83);

            // Format in Indian numbering system
            const formatINR = (num) => {
                if (num >= 10000000) {
                    return `₹${(num / 10000000).toFixed(2)} Cr`;
                } else if (num >= 100000) {
                    return `₹${(num / 100000).toFixed(1)} LPA`;
                } else {
                    return `₹${(num / 1000).toFixed(0)}K`;
                }
            };

            return `${formatINR(minINR)} - ${formatINR(maxINR)}`;
        } catch (error) {
            console.error('Error converting salary:', error);
            return salaryRange;
        }
    };

    const handleBackToHome = () => {
        try {
            // Clear analysis data if reset function exists
            if (onReset) {
                onReset();
            }

            // Navigate to home page
            navigate('/');

            // Force page reload to ensure clean state
            window.location.href = '/';
        } catch (error) {
            console.error('Error navigating home:', error);
            // Fallback navigation
            window.location.href = '/';
        }
    };

    const handleViewReport = () => {
        navigate('/report', { state: { data } });
    };

    return (
        <div className="dashboard-container">
            <div className="container">
                {/* Header */}
                <div className="dashboard-header fade-in">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', marginBottom: '20px' }}>
                        <button
                            onClick={handleBackToHome}
                            className="back-button"
                            type="button"
                            style={{ cursor: 'pointer', zIndex: 1000, pointerEvents: 'auto' }}
                        >
                            🏠 ← Back to Home
                        </button>
                        <button
                            onClick={handleViewReport}
                            className="back-button" // Reuse style for consistency
                            style={{
                                cursor: 'pointer',
                                zIndex: 1000,
                                pointerEvents: 'auto',
                                background: 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)',
                                border: 'none'
                            }}
                        >
                            📄 View & Download Report
                        </button>
                    </div>
                    <h1>Your Career Intelligence Report</h1>
                    <p>AI-Powered Personalized Career Guidance</p>
                </div>

                {/* Main Recommendation Card */}
                <div className="recommendation-card glass-card-glow scale-in">
                    <div className="recommendation-header">
                        <div className="career-icon">🎯</div>
                        <div>
                            <h2>{career_recommendation.career}</h2>
                            <p className="career-description">{career_recommendation.description}</p>
                        </div>
                    </div>

                    <div className="confidence-score">
                        <div className="score-circle">
                            <svg viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="45" className="score-bg" />
                                <circle
                                    cx="50"
                                    cy="50"
                                    r="45"
                                    className="score-fill"
                                    style={{
                                        strokeDasharray: `${career_recommendation.confidence_score * 2.827} 282.7`
                                    }}
                                />
                            </svg>
                            <div className="score-text">
                                <span className="score-number">{Math.round(career_recommendation.confidence_score)}</span>
                                <span className="score-label">Match</span>
                            </div>
                        </div>
                        <div className="score-details">
                            <h3>Why This Career Fits You</h3>
                            <p className="reasoning">{career_recommendation.reasoning}</p>
                        </div>
                    </div>

                    <div className="career-stats">
                        <div className="stat-card">
                            <div className="stat-icon">💰</div>
                            <div className="stat-content">
                                <div className="stat-label">Salary Range (India)</div>
                                <div className="stat-value">{convertToINR(career_recommendation.salary_range)}</div>
                            </div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-icon">📈</div>
                            <div className="stat-content">
                                <div className="stat-label">Growth Potential</div>
                                <div className="stat-value">{career_recommendation.growth_potential}</div>
                            </div>
                        </div>
                        <div className="stat-card">
                            <div className="stat-icon">🎓</div>
                            <div className="stat-content">
                                <div className="stat-label">Readiness</div>
                                <div className="stat-value">
                                    {skill_analysis.industry_comparison.current_level}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tab Navigation */}
                <div className="tab-navigation">
                    <button
                        className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
                        onClick={() => setActiveTab('overview')}
                    >
                        Overview
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'skills' ? 'active' : ''}`}
                        onClick={() => setActiveTab('skills')}
                    >
                        Analytics & Skills
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'roadmap' ? 'active' : ''}`}
                        onClick={() => setActiveTab('roadmap')}
                    >
                        Learning Roadmap
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'alternatives' ? 'active' : ''}`}
                        onClick={() => setActiveTab('alternatives')}
                    >
                        Alternative Paths
                    </button>
                </div>

                {/* Tab Content */}
                <div className="tab-content">
                    {activeTab === 'overview' && (
                        <div className="overview-tab fade-in">
                            <div className="overview-grid">
                                {/* Job Roles */}
                                <div className="glass-card">
                                    <h3>🎯 Recommended Job Roles</h3>
                                    <div className="job-roles-list">
                                        {career_recommendation.job_roles.map((role, index) => (
                                            <div key={index} className="job-role-item">
                                                <span className="role-bullet">•</span>
                                                {role}
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Top Companies */}
                                <div className="glass-card">
                                    <h3>🏢 Top Companies Hiring</h3>
                                    <div className="companies-grid">
                                        {career_recommendation.companies.slice(0, 8).map((company, index) => (
                                            <div key={index} className="company-badge">
                                                {company}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Quick Wins */}
                            {skill_analysis.quick_wins && skill_analysis.quick_wins.length > 0 && (
                                <div className="glass-card quick-wins-card">
                                    <h3>⚡ Quick Wins - Skills You Can Learn Fast</h3>
                                    <div className="quick-wins-list">
                                        {skill_analysis.quick_wins.map((win, index) => (
                                            <div key={index} className="quick-win-item">
                                                <div className="quick-win-header">
                                                    <span className="quick-win-skill">{win.skill}</span>
                                                    <span className="badge badge-success">{win.estimated_time}</span>
                                                </div>
                                                <p className="quick-win-reason">{win.reason}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {activeTab === 'skills' && (
                        <div className="skills-tab fade-in">
                            <div className="charts-grid" style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '30px' }}>
                                <SalaryComparisonChart
                                    recommended={career_recommendation}
                                    alternatives={alternative_careers}
                                />
                                <SkillGapChart data={skill_analysis} />
                            </div>
                        </div>
                    )}

                    {activeTab === 'roadmap' && (
                        <div className="roadmap-tab fade-in">
                            <LearningRoadmap data={learning_roadmap} />
                        </div>
                    )}

                    {activeTab === 'alternatives' && (
                        <div className="alternatives-tab fade-in">
                            <AlternativePaths data={alternative_careers} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default CareerDashboard;
