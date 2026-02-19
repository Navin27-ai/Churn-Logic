/**
 * Main Application
 * Handles navigation, initialization, and global state
 */

console.log('✅ ChurnLogic App Loaded');

// Global State
const appState = {
    currentPage: 'dashboard',
    isDarkMode: localStorage.getItem('theme') === 'dark',
    userData: null,
    dashboardData: null
};

/**
 * Load a page by name
 */
function loadPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    const page = document.getElementById(`${pageName}-page`);
    if (page) {
        page.classList.add('active');
    }
    
    // Update nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeNav = document.querySelector(`[data-page="${pageName}"]`);
    if (activeNav) {
        activeNav.classList.add('active');
    }
    
    // Update title
    const titles = {
        'dashboard': 'Dashboard',
        'upload': 'Upload Data',
        'churn-analysis': 'Churn Analysis',
        'behavior': 'Behavior Analytics',
        'simulation': 'Simulation Studio',
        'strategy': 'AI Strategy',
        'insights': 'Insights'
    };
    
    const titleElement = document.querySelector('.page-title');
    if (titleElement) {
        titleElement.textContent = titles[pageName] || 'Dashboard';
    }
    
    appState.currentPage = pageName;
    
    // Load page-specific content
    if (pageName === 'dashboard') {
        loadDashboard();
    }
}

/**
 * Upload file
 */
function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    
    if (!fileInput || !fileInput.files[0]) {
        showToast('Please select a file', 'warning');
        return;
    }
    
    const file = fileInput.files[0];
    
    // Validate file
    if (!file.name.endsWith('.csv')) {
        showToast('Please upload a CSV file', 'danger');
        return;
    }
    
    // Show loading state
    const uploadBtn = document.querySelector('button[onclick="uploadFile()"]');
    if (uploadBtn) {
        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Uploading...';
    }
    
    // Upload
    api.uploadDataset(file).then(response => {
        if (uploadBtn) {
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload';
        }
        
        if (response && response.status === 'success') {
            showToast(`File uploaded successfully! ${response.rows} rows, ${response.columns} columns`, 'success');
            fileInput.value = '';
            console.log('Upload response:', response);
        } else {
            showToast('Upload failed', 'danger');
        }
    });
}

/**
 * Load dashboard data
 */
function loadDashboard() {
    api.getDashboardData().then(data => {
        if (data) {
            updateDashboard(data);
            appState.dashboardData = data;
            console.log('Dashboard data:', data);
        }
    });
}

/**
 * Update dashboard with data
 */
function updateDashboard(data) {
    const kpiCards = document.querySelectorAll('.kpi-card');
    
    if (kpiCards.length >= 4) {
        kpiCards[0].querySelector('.kpi-value').textContent = data.total_customers || 0;
        kpiCards[1].querySelector('.kpi-value').textContent = (data.churn_rate || 0).toFixed(1) + '%';
        kpiCards[2].querySelector('.kpi-value').textContent = data.at_risk_customers || 0;
        kpiCards[3].querySelector('.kpi-value').textContent = (data.avg_churn_score || 0).toFixed(2);
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.animation = 'slideDown 0.3s ease-out';
    
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideUp 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
    appState.isDarkMode = !appState.isDarkMode;
    document.body.classList.toggle('dark-mode');
    
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = appState.isDarkMode ? '☀️' : '🌙';
    }
    
    localStorage.setItem('theme', appState.isDarkMode ? 'dark' : 'light');
}

/**
 * Initialize app
 */
function initializeApp() {
    console.log('📊 Initializing ChurnLogic...');
    
    // Setup nav click handlers
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            if (page) {
                loadPage(page);
            }
        });
    });
    
    // Setup theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleDarkMode);
        
        // Load saved theme
        if (appState.isDarkMode) {
            document.body.classList.add('dark-mode');
            themeToggle.textContent = '☀️';
        }
    }
    
    // Load initial dashboard
    loadDashboard();
    
    console.log('✅ ChurnLogic Ready!');
}

/**
 * On DOM load
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/**
 * Global error handler
 */
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    showToast('An error occurred', 'danger');
});