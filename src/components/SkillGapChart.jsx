import { useEffect, useRef } from 'react';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';
import { Radar } from 'react-chartjs-2';
import './SkillGapChart.css';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

function SkillGapChart({ data }) {
    const { gap_analysis, industry_comparison } = data;
    const { skills_analysis, metrics } = gap_analysis;

    // Prepare data for radar chart
    const allSkills = [
        ...skills_analysis.possessed.map(s => s.skill),
        ...skills_analysis.missing_critical.map(s => s.skill),
        ...skills_analysis.missing_important.map(s => s.skill)
    ].slice(0, 8); // Limit to 8 skills for readability

    const userScores = allSkills.map(skill => {
        const possessed = skills_analysis.possessed.find(s => s.skill === skill);
        return possessed ? 10 : 0;
    });

    const requiredScores = allSkills.map(() => 10);

    const chartData = {
        labels: allSkills,
        datasets: [
            {
                label: 'Your Skills',
                data: userScores,
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(102, 126, 234, 1)',
            },
            {
                label: 'Industry Standard',
                data: requiredScores,
                backgroundColor: 'rgba(245, 87, 108, 0.2)',
                borderColor: 'rgba(245, 87, 108, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(245, 87, 108, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(245, 87, 108, 1)',
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            r: {
                angleLines: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                pointLabels: {
                    color: '#b8c1ec',
                    font: {
                        size: 12,
                        weight: 600
                    }
                },
                ticks: {
                    display: false
                },
                suggestedMin: 0,
                suggestedMax: 10
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: '#b8c1ec',
                    font: {
                        size: 14
                    }
                }
            }
        }
    };

    return (
        <div className="skill-gap-container">
            {/* Metrics Overview */}
            <div className="metrics-grid">
                <div className="metric-card glass-card">
                    <div className="metric-icon">✓</div>
                    <div className="metric-content">
                        <div className="metric-value">{metrics.possessed_skills}</div>
                        <div className="metric-label">Skills Possessed</div>
                    </div>
                </div>
                <div className="metric-card glass-card">
                    <div className="metric-icon">⚠</div>
                    <div className="metric-content">
                        <div className="metric-value">{metrics.missing_skills}</div>
                        <div className="metric-label">Skills to Learn</div>
                    </div>
                </div>
                <div className="metric-card glass-card">
                    <div className="metric-icon">📊</div>
                    <div className="metric-content">
                        <div className="metric-value">{Math.round(metrics.readiness_score)}%</div>
                        <div className="metric-label">Readiness Score</div>
                    </div>
                </div>
            </div>

            {/* Radar Chart */}
            <div className="glass-card chart-container">
                <h3>Skill Gap Visualization</h3>
                <div className="radar-chart">
                    <Radar data={chartData} options={chartOptions} />
                </div>
            </div>

            {/* Industry Comparison */}
            <div className="glass-card industry-comparison">
                <h3>Industry Benchmark Comparison</h3>
                <div className="benchmark-info">
                    <div className="current-level">
                        <span className="level-label">Your Current Level:</span>
                        <span className="level-badge badge-primary">{industry_comparison.current_level}</span>
                    </div>
                    <p className="benchmark-message">{industry_comparison.message}</p>
                </div>

                <div className="benchmark-progress">
                    <div className="benchmark-bar">
                        <div className="benchmark-markers">
                            <div className="marker" style={{ left: '40%' }}>
                                <span className="marker-label">Entry</span>
                            </div>
                            <div className="marker" style={{ left: '70%' }}>
                                <span className="marker-label">Mid</span>
                            </div>
                            <div className="marker" style={{ left: '90%' }}>
                                <span className="marker-label">Senior</span>
                            </div>
                        </div>
                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{ width: `${industry_comparison.readiness_score}%` }}
                            >
                                <span className="progress-label">
                                    {Math.round(industry_comparison.readiness_score)}%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                {industry_comparison.next_milestone && (
                    <div className="next-milestone">
                        <h4>Next Milestone: {industry_comparison.next_milestone.target}</h4>
                        <p>{industry_comparison.next_milestone.message}</p>
                    </div>
                )}
            </div>

            {/* Skill Breakdown */}
            <div className="skills-breakdown">
                {/* Critical Skills */}
                {skills_analysis.missing_critical.length > 0 && (
                    <div className="glass-card skill-category">
                        <h3>🔴 Critical Skills (High Priority)</h3>
                        <div className="skills-list">
                            {skills_analysis.missing_critical.map((skill, index) => (
                                <div key={index} className="skill-item critical">
                                    <span className="skill-name">{skill.skill}</span>
                                    <span className="skill-weight">Weight: {skill.weight}/10</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Important Skills */}
                {skills_analysis.missing_important.length > 0 && (
                    <div className="glass-card skill-category">
                        <h3>🟡 Important Skills (Medium Priority)</h3>
                        <div className="skills-list">
                            {skills_analysis.missing_important.map((skill, index) => (
                                <div key={index} className="skill-item important">
                                    <span className="skill-name">{skill.skill}</span>
                                    <span className="skill-weight">Weight: {skill.weight}/10</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Nice to Have Skills */}
                {skills_analysis.missing_nice_to_have.length > 0 && (
                    <div className="glass-card skill-category">
                        <h3>🟢 Nice-to-Have Skills (Low Priority)</h3>
                        <div className="skills-list">
                            {skills_analysis.missing_nice_to_have.map((skill, index) => (
                                <div key={index} className="skill-item nice">
                                    <span className="skill-name">{skill.skill}</span>
                                    <span className="skill-weight">Weight: {skill.weight}/10</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Possessed Skills */}
                {skills_analysis.possessed.length > 0 && (
                    <div className="glass-card skill-category">
                        <h3>✅ Your Current Skills</h3>
                        <div className="skills-list">
                            {skills_analysis.possessed.map((skill, index) => (
                                <div key={index} className="skill-item possessed">
                                    <span className="skill-name">{skill.skill}</span>
                                    <span className="skill-badge badge-success">Mastered</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default SkillGapChart;
