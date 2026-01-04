/**
 * auth.js
 * Handles user authentication, session storage, and route protection.
 */

const Auth = {
    // API Endpoint Base
    // Assuming backend is on the same host/port if served by Flask, 
    // or we might need to specify full URL if running separately.
    // Given the setup, relative paths like '/login' should work if served by Flask.
    // If opening HTML directly, we need the full URL (e.g. http://localhost:5000)
    // For this environment, let's assume relative paths if served, but fallback to localhost:5000 if needed.
    // Since the USER puts files in 'dashboard' folder, likely opening via file:// or served by Flask static.
    // app.py doesn't seem to serve "dashboard" folder at root, but user might be opening HTML files directly.
    // We will assume localhost:5000 for API calls to be safe.
    API_URL: 'http://localhost:5000',

    /**
     * Login User
     * @param {string} username 
     * @param {string} password 
     */
    async login(username, password) {
        try {
            const response = await fetch(`${this.API_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                // Save user session
                const user = { username: data.username || username };
                localStorage.setItem('agri_user', JSON.stringify(user));
                return { success: true };
            } else {
                return { success: false, message: data.error || 'Login failed' };
            }
        } catch (error) {
            console.error('Login Error:', error);
            return { success: false, message: 'Server connection failed' };
        }
    },

    /**
     * Logout User
     */
    logout() {
        localStorage.removeItem('agri_user');
        window.location.href = 'login.html';
    },

    /**
     * Check if user is authenticated
     * Redirects to login if not.
     * @returns {object|null} User object or null
     */
    check() {
        const userStr = localStorage.getItem('agri_user');
        if (!userStr) {
            // Not logged in
            // Redirect only if not already on login page
            if (!window.location.pathname.includes('login.html')) {
                window.location.href = 'login.html';
            }
            return null;
        }
        return JSON.parse(userStr);
    }
};

// Expose to window
window.Auth = Auth;
