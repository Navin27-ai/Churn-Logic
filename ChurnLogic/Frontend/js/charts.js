/**
 * Chart Manager
 * Handles chart creation and management
 */

class ChartManager {
    constructor() {
        this.charts = {};
        this.defaultColors = [
            '#7c3aed',
            '#06b6d4',
            '#f59e0b',
            '#10b981',
            '#ef4444',
            '#ec4899',
            '#8b5cf6',
            '#06b6d4'
        ];
    }

    /**
     * Create a chart
     */
    createChart(elementId, type, config) {
        const ctx = document.getElementById(elementId);
        if (!ctx) {
            console.warn(`Chart element not found: ${elementId}`);
            return null;
        }

        // Destroy existing chart
        if (this.charts[elementId]) {
            this.charts[elementId].destroy();
        }

        // Create new chart
        this.charts[elementId] = new Chart(ctx, {
            type: type,
            data: config.data,
            options: {
                responsive: true,
                maintainAspectRatio: config.maintainAspectRatio !== false,
                plugins: {
                    legend: config.legend || {
                        display: true,
                        position: 'bottom'
                    }
                },
                scales: config.scales || {}
            }
        });

        return this.charts[elementId];
    }

    /**
     * Create line chart
     */
    createLineChart(elementId, labels, datasets) {
        return this.createChart(elementId, 'line', {
            data: {
                labels: labels,
                datasets: datasets.map((dataset, index) => ({
                    label: dataset.label,
                    data: dataset.data,
                    borderColor: this.defaultColors[index % this.defaultColors.length],
                    backgroundColor: `rgba(124, 58, 237, 0.1)`,
                    tension: 0.3,
                    fill: false
                }))
            }
        });
    }

    /**
     * Create bar chart
     */
    createBarChart(elementId, labels, datasets) {
        return this.createChart(elementId, 'bar', {
            data: {
                labels: labels,
                datasets: datasets.map((dataset, index) => ({
                    label: dataset.label,
                    data: dataset.data,
                    backgroundColor: this.defaultColors[index % this.defaultColors.length]
                }))
            }
        });
    }

    /**
     * Create pie chart
     */
    createPieChart(elementId, labels, data) {
        return this.createChart(elementId, 'pie', {
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: this.defaultColors
                }]
            }
        });
    }

    /**
     * Create doughnut chart
     */
    createDoughnutChart(elementId, labels, data) {
        return this.createChart(elementId, 'doughnut', {
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: this.defaultColors
                }]
            }
        });
    }

    /**
     * Destroy a chart
     */
    destroyChart(elementId) {
        if (this.charts[elementId]) {
            this.charts[elementId].destroy();
            delete this.charts[elementId];
        }
    }

    /**
     * Destroy all charts
     */
    destroyAll() {
        Object.keys(this.charts).forEach(key => {
            this.charts[key].destroy();
        });
        this.charts = {};
    }

    /**
     * Update chart data
     */
    updateChartData(elementId, data) {
        if (this.charts[elementId]) {
            this.charts[elementId].data.datasets[0].data = data;
            this.charts[elementId].update();
        }
    }

    /**
     * Export chart as image
     */
    exportChart(elementId, filename = 'chart.png') {
        if (this.charts[elementId]) {
            const canvas = this.charts[elementId].canvas;
            const link = document.createElement('a');
            link.href = canvas.toDataURL('image/png');
            link.download = filename;
            link.click();
        }
    }
}

// Initialize chart manager
const chartManager = new ChartManager();