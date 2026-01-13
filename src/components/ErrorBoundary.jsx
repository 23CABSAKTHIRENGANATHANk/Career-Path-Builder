import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        this.setState({
            error: error,
            errorInfo: errorInfo
        });
    }

    handleReset = () => {
        this.setState({ hasError: false, error: null, errorInfo: null });
        window.location.href = '/';
    };

    render() {
        if (this.state.hasError) {
            return (
                <div style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '100vh',
                    backgroundColor: '#0f172a',
                    color: 'white',
                    padding: '20px'
                }}>
                    <div style={{
                        maxWidth: '600px',
                        padding: '40px',
                        background: 'rgba(255,255,255,0.1)',
                        borderRadius: '16px',
                        border: '1px solid rgba(255,255,255,0.2)',
                        textAlign: 'center'
                    }}>
                        <h1 style={{ fontSize: '2.5rem', marginBottom: '20px' }}>⚠️ Something Went Wrong</h1>
                        <p style={{ fontSize: '1.1rem', marginBottom: '20px', color: '#cbd5e1' }}>
                            An unexpected error occurred in the application.
                        </p>
                        {this.state.error && (
                            <details style={{
                                marginBottom: '20px',
                                padding: '15px',
                                background: 'rgba(0,0,0,0.3)',
                                borderRadius: '8px',
                                textAlign: 'left',
                                maxHeight: '200px',
                                overflowY: 'auto'
                            }}>
                                <summary style={{ cursor: 'pointer', marginBottom: '10px', color: '#f5576c' }}>
                                    Error Details
                                </summary>
                                <pre style={{ fontSize: '0.8rem', color: '#94a3b8', overflow: 'auto' }}>
                                    {this.state.error.toString()}
                                </pre>
                            </details>
                        )}
                        <button
                            onClick={this.handleReset}
                            style={{
                                padding: '14px 28px',
                                fontSize: '1rem',
                                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                color: 'white',
                                border: 'none',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                fontWeight: 'bold',
                                marginRight: '10px'
                            }}
                        >
                            🏠 Return to Home
                        </button>
                        <button
                            onClick={() => window.location.reload()}
                            style={{
                                padding: '14px 28px',
                                fontSize: '1rem',
                                background: 'transparent',
                                color: '#94a3b8',
                                border: '1px solid rgba(255,255,255,0.3)',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                fontWeight: 'bold'
                            }}
                        >
                            🔄 Reload Page
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
