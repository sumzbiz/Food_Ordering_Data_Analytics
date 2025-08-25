// Main JavaScript file for Zomato-like App

// Utility functions
const Utils = {
    // Format currency
    formatCurrency: function(amount) {
        return '₹' + parseFloat(amount).toFixed(2);
    },
    
    // Show toast notification
    showToast: function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    },
    
    // Validate email format
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    // Validate phone number
    isValidPhone: function(phone) {
        const phoneRegex = /^[0-9]{10}$/;
        return phoneRegex.test(phone);
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    // Format datetime
    formatDateTime: function(date) {
        return new Date(date).toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
};

// Cart management
const Cart = {
    items: {},
    
    addItem: function(itemId, quantity = 1) {
        if (this.items[itemId]) {
            this.items[itemId] += quantity;
        } else {
            this.items[itemId] = quantity;
        }
        this.updateDisplay();
    },
    
    removeItem: function(itemId) {
        delete this.items[itemId];
        this.updateDisplay();
    },
    
    updateQuantity: function(itemId, quantity) {
        if (quantity <= 0) {
            this.removeItem(itemId);
        } else {
            this.items[itemId] = quantity;
        }
        this.updateDisplay();
    },
    
    clear: function() {
        this.items = {};
        this.updateDisplay();
    },
    
    getTotal: function() {
        let total = 0;
        for (const itemId in this.items) {
            const price = this.getItemPrice(itemId);
            total += price * this.items[itemId];
        }
        return total;
    },
    
    getItemPrice: function(itemId) {
        // This would typically come from the server
        const prices = {
            1: 180.00, // Biriyani
            2: 150.00, // Paneer
            3: 200.00, // Butter Chicken
            4: 90.00,  // Veg Momos
            5: 120.00  // Chicken Wings
        };
        return prices[itemId] || 0;
    },
    
    updateDisplay: function() {
        // This will be implemented in specific pages
        if (typeof updateCartDisplay === 'function') {
            updateCartDisplay();
        }
    }
};

// Form validation
const FormValidator = {
    validateRequired: function(value, fieldName) {
        if (!value || value.trim() === '') {
            return `${fieldName} is required`;
        }
        return null;
    },
    
    validateEmail: function(email) {
        if (email && !Utils.isValidEmail(email)) {
            return 'Please enter a valid email address';
        }
        return null;
    },
    
    validatePhone: function(phone) {
        if (phone && !Utils.isValidPhone(phone)) {
            return 'Please enter a valid 10-digit phone number';
        }
        return null;
    },
    
    validateLength: function(value, minLength, maxLength, fieldName) {
        if (value && (value.length < minLength || value.length > maxLength)) {
            return `${fieldName} must be between ${minLength} and ${maxLength} characters`;
        }
        return null;
    },
    
    validateNumber: function(value, fieldName, min = null, max = null) {
        const num = parseFloat(value);
        if (isNaN(num)) {
            return `${fieldName} must be a valid number`;
        }
        if (min !== null && num < min) {
            return `${fieldName} must be at least ${min}`;
        }
        if (max !== null && num > max) {
            return `${fieldName} must be at most ${max}`;
        }
        return null;
    }
};

// API helper
const API = {
    baseURL: '',
    
    request: function(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
            }
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        return fetch(url, finalOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('API request failed:', error);
                throw error;
            });
    },
    
    get: function(url) {
        return this.request(url);
    },
    
    post: function(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    put: function(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    delete: function(url) {
        return this.request(url, {
            method: 'DELETE'
        });
    }
};

// Page initialization
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add loading states to buttons
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            }
        });
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add responsive table wrapper
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
});

// Export for use in other scripts
window.Utils = Utils;
window.Cart = Cart;
window.FormValidator = FormValidator;
window.API = API;
