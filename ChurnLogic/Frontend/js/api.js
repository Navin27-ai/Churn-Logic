/**
 * API Service
 * Handles all backend API calls
 */

const API_BASE_URL = 'http://localhost:8000/api';

const api = {
    /**
     * GET request
     */
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            return null;
        }
    },

    /**
     * POST request with JSON
     */
    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            return null;
        }
    },

    /**
     * File upload
     */
    async uploadFile(endpoint, file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Upload Error:', error);
            return null;
        }
    },

    /**
     * GET Dashboard Data
     */
    async getDashboardData() {
        return this.get('/dashboard-data');
    },

    /**
     * Upload CSV File
     */
    async uploadDataset(file) {
        return this.uploadFile('/upload-data', file);
    },

    /**
     * Train Model
     */
    async trainModel() {
        return this.post('/train-model', {});
    },

    /**
     * Get Predictions
     */
    async getPredictions() {
        return this.get('/predict-churn');
    },

    /**
     * Get Model Metrics
     */
    async getModelMetrics() {
        return this.get('/model-metrics');
    },

    /**
     * Get Feature Importance
     */
    async getFeatureImportance() {
        return this.get('/feature-importance');
    },

    /**
     * Cluster Customers
     */
    async clusterCustomers() {
        return this.post('/cluster-users', {});
    },

    /**
     * Get Cluster Summary
     */
    async getClusterSummary() {
        return this.get('/cluster-summary');
    },

    /**
     * Simulate Scenario
     */
    async simulateScenario(params) {
        return this.post('/simulate-scenario', params);
    },

    /**
     * Generate Retention Strategy
     */
    async generateRetentionStrategy() {
        return this.post('/generate-retention-strategy', {});
    }
};