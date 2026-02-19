/**
 * Dashboard Manager
 * Handles dashboard functionality
 */

class DashboardManager {
    constructor() {
        this.currentPage = 'dashboard';
        this.charts = {};
        this.refreshInterval = null;
    }

    /**
     * Load dashboard
     */
    loadDashboard() {
        console.log('📊 Loading dashboard...');
        api.getDashboardData().then(data => {
            if (data) {
                this.updateDashboard(data);
                this.renderCharts(data);
            }
        });
    }

    /**
     * Update dashboard KPIs
     */
    updateDashboard(data) {
        const kpiCards = document.querySelectorAll('.kpi-card');
        
        if (kpiCards.length >= 4) {
            // Total Customers
            const totalCustomers = data.total_customers || 0;
            kpiCards[0].querySelector('.kpi-value').textContent = totalCustomers.toLocaleString();
            
            // Churn Rate
            const churnRate = (data.churn_rate || 0).toFixed(1);
            kpiCards[1].querySelector('.kpi-value').textContent = churnRate + '%';
            
            // At-Risk Customers
            const atRisk = data.at_risk_customers || 0;
            kpiCards[2].querySelector('.kpi-value').textContent = atRisk.toLocaleString();
            
            // Avg Churn Score
            const avgScore = (data.avg_churn_score || 0).toFixed(2);
            kpiCards[3].querySelector('.kpi-value').textContent = avgScore;
        }
    }

    /**
     * Render charts
     */
    renderCharts(data) {
        // Churn Distribution Chart
        if (data.churn_distribution && data.churn_distribution.length > 0) {
            this.createChurnDistributionChart(data.churn_distribution);
        }
        
        // Retention by Segment
        if (data.retention_by_segment && data.retention_by_segment.length > 0) {
            this.createRetentionChart(data.retention_by_segment);
        }
        
        // Behavior Segments
        if (data.behavior_segments && data.behavior_segments.length > 0) {
            this.createBehaviorChart(data.behavior_segments);
        }
    }

    /**
     * Create churn distribution chart
     */
    createChurnDistributionChart(data) {
        const ctx = document.getElementById('churnDistributionChart');
        if (!ctx) return;
        
        if (this.charts['churnDistribution']) {
            this.charts['churnDistribution'].destroy();
        }
        
        this.charts['churnDistribution'] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.label),
                datasets: [{
                    data: data.map(d => d.value),
                    backgroundColor: ['#ef4444', '#10b981'],
                    borderColor: 'var(--bg-primary)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    /**
     * Create retention by segment chart
     */
    createRetentionChart(data) {
        const ctx = document.getElementById('retentionChart');
        if (!ctx) return;
        
        if (this.charts['retention']) {
            this.charts['retention'].destroy();
        }
        
        this.charts['retention'] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.segment),
                datasets: [{
                    label: 'Retention Rate (%)',
                    data: data.map(d => d.retention_rate),
                    backgroundColor: '#7c3aed',
                    borderColor: '#7c3aed',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    /**
     * Create behavior segments chart
     */
    createBehaviorChart(data) {
        const ctx = document.getElementById('behaviorChart');
        if (!ctx) return;
        
        if (this.charts['behavior']) {
            this.charts['behavior'].destroy();
        }
        
        this.charts['behavior'] = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.map(d => d.segment),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: [
                        '#7c3aed',
                        '#06b6d4',
                        '#f59e0b',
                        '#10b981'
                    ],
                    borderColor: 'var(--bg-primary)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }

    /**
     * Start auto-refresh
     */
    startAutoRefresh(interval = 30000) {
        this.refreshInterval = setInterval(() => {
            this.loadDashboard();
        }, interval);
    }

    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
    }

    /**
     * Export dashboard as PDF (placeholder)
     */
    exportDashboard() {
        console.log('Exporting dashboard...');
        showToast('Dashboard export feature coming soon!', 'info');
    }
}

// Initialize dashboard manager
const dashboardManager = new DashboardManager();

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    dashboardManager.loadDashboard();
});