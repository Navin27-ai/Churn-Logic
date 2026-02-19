/**
 * Utility Functions
 * Common helpers used throughout the app
 */

const utils = {
    /**
     * Format number as currency
     */
    formatCurrency(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(value);
    },

    /**
     * Format as percentage
     */
    formatPercentage(value, decimals = 2) {
        return (value * 100).toFixed(decimals) + '%';
    },

    /**
     * Format number with commas
     */
    formatNumber(value) {
        return Number(value).toLocaleString('en-US', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        });
    },

    /**
     * Format date
     */
    formatDate(date, format = 'short') {
        const d = new Date(date);
        
        if (format === 'short') {
            return d.toLocaleDateString('en-US');
        } else if (format === 'long') {
            return d.toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } else if (format === 'time') {
            return d.toLocaleTimeString('en-US');
        }
        
        return d.toString();
    },

    /**
     * Check if value is empty
     */
    isEmpty(value) {
        return value === undefined || value === null || value === '';
    },

    /**
     * Deep clone object
     */
    cloneObject(obj) {
        return JSON.parse(JSON.stringify(obj));
    },

    /**
     * Merge objects
     */
    mergeObjects(obj1, obj2) {
        return { ...obj1, ...obj2 };
    },

    /**
     * Sort array of objects
     */
    sortByProperty(arr, property, ascending = true) {
        return arr.sort((a, b) => {
            if (ascending) {
                return a[property] > b[property] ? 1 : -1;
            } else {
                return a[property] < b[property] ? 1 : -1;
            }
        });
    },

    /**
     * Filter array of objects
     */
    filterByProperty(arr, property, value) {
        return arr.filter(item => item[property] === value);
    },

    /**
     * Group array by property
     */
    groupByProperty(arr, property) {
        return arr.reduce((grouped, item) => {
            const key = item[property];
            if (!grouped[key]) {
                grouped[key] = [];
            }
            grouped[key].push(item);
            return grouped;
        }, {});
    },

    /**
     * Generate random ID
     */
    generateId() {
        return '_' + Math.random().toString(36).substr(2, 9);
    },

    /**
     * Debounce function
     */
    debounce(func, delay) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    },

    /**
     * Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function (...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    /**
     * Parse CSV string
     */
    parseCSV(csvString) {
        const lines = csvString.split('\n');
        const headers = lines[0].split(',');
        const data = [];
        
        for (let i = 1; i < lines.length; i++) {
            if (lines[i].trim() === '') continue;
            
            const obj = {};
            const currentline = lines[i].split(',');
            
            for (let j = 0; j < headers.length; j++) {
                obj[headers[j].trim()] = currentline[j].trim();
            }
            
            data.push(obj);
        }
        
        return data;
    },

    /**
     * Copy to clipboard
     */
    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy', 'danger');
        });
    },

    /**
     * Get query parameter
     */
    getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    },

    /**
     * Validate email
     */
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    /**
     * Calculate percentage
     */
    calculatePercentage(value, total) {
        return (value / total) * 100;
    },

    /**
     * Sleep function
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    /**
     * Get local storage item
     */
    getFromStorage(key) {
        const item = localStorage.getItem(key);
        try {
            return item ? JSON.parse(item) : null;
        } catch (e) {
            return item;
        }
    },

    /**
     * Save to local storage
     */
    saveToStorage(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Storage error:', e);
        }
    },

    /**
     * Remove from storage
     */
    removeFromStorage(key) {
        localStorage.removeItem(key);
    },

    /**
     * Clear all storage
     */
    clearStorage() {
        localStorage.clear();
    }
};