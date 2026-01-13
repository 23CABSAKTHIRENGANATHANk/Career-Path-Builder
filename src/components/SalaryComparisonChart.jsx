
import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const SalaryComparisonChart = ({ recommended, alternatives }) => {
    // Helper to parse salary average
    const getAverageSalary = (salaryStr) => {
        if (!salaryStr) return 0;
        try {
            // Remove non-numeric chars except dash
            const numbers = salaryStr.replace(/[$,]/g, '').match(/(\d+)/g);
            if (numbers && numbers.length >= 2) {
                return (parseInt(numbers[0]) + parseInt(numbers[1])) / 2;
            }
            return 0;
        } catch (e) {
            return 0;
        }
    };

    const labels = [recommended.career, ...alternatives.map(a => a.career)];
    const dataPoints = [
        getAverageSalary(recommended.salary_range),
        ...alternatives.map(a => getAverageSalary(a.salary_range || recommended.salary_range)) // Fallback if alt has no salary
    ];

    const data = {
        labels,
        datasets: [
            {
                label: 'Average Annual Salary (USD Estimate)',
                data: dataPoints,
                backgroundColor: [
                    'rgba(139, 92, 246, 0.8)', // Primary (Recommended)
                    'rgba(59, 130, 246, 0.5)', // Alternative 1
                    'rgba(59, 130, 246, 0.5)', // Alternative 2
                    'rgba(59, 130, 246, 0.5)', // Alternative 3
                ],
                borderColor: [
                    'rgba(139, 92, 246, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(59, 130, 246, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    const options = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Market Value Comparison',
                color: '#fff',
                font: {
                    size: 16
                }
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.x !== null) {
                            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.x);
                        }
                        return label;
                    }
                }
            }
        },
        scales: {
            x: {
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: {
                    color: '#ccc',
                    callback: function (value, index, values) {
                        return '$' + value / 1000 + 'k';
                    }
                }
            },
            y: {
                grid: { display: false },
                ticks: { color: '#fff' }
            }
        }
    };

    return (
        <div style={{ height: '300px', padding: '20px', background: 'rgba(0,0,0,0.2)', borderRadius: '15px' }}>
            <Bar options={options} data={data} />
        </div>
    );
};

export default SalaryComparisonChart;
