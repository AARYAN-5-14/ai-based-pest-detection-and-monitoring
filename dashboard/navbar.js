/**
 * navbar.js
 * Handles Sidebar and Navbar injection and interaction logic.
 */

// Mapping active page to an identifier
const PAGE_IDS = {
    'index.html': 'dashboard',
    'history.html': 'history',
    'alerts.html': 'alerts',
    'reports.html': 'reports'
};

function injectLayout(activePageId) {
    const wrapper = document.getElementById('wrapper');
    if (!wrapper) return;

    // 1. Inject Sidebar
    const sidebarHTML = `
        <div class="sidebar-heading">
            <span><i class="fas fa-leaf me-2"></i>AgriGuard</span>
            <span class="d-md-none" id="sidebarClose" style="cursor:pointer;"><i class="fas fa-times"></i></span>
        </div>
        <div class="list-group list-group-flush mt-3">
            <a href="index.html" class="list-group-item list-group-item-action ${activePageId === 'dashboard' ? 'active' : ''}">
                <i class="fas fa-th-large me-3"></i>Dashboard
            </a>
            <a href="history.html" class="list-group-item list-group-item-action ${activePageId === 'history' ? 'active' : ''}">
                <i class="fas fa-list-alt me-3"></i>Pest History
            </a>
            <a href="alerts.html" class="list-group-item list-group-item-action ${activePageId === 'alerts' ? 'active' : ''}">
                <i class="fas fa-exclamation-triangle me-3"></i>Alerts
            </a>
            <a href="reports.html" class="list-group-item list-group-item-action ${activePageId === 'reports' ? 'active' : ''}">
                <i class="fas fa-file-download me-3"></i>Reports
            </a>
            <a href="#" onclick="Auth.logout()" class="list-group-item list-group-item-action mt-auto text-danger-custom" style="border-top:1px solid rgba(255,255,255,0.1)">
                <i class="fas fa-sign-out-alt me-3"></i>Logout
            </a>
        </div>
    `;

    const sidebarDiv = document.createElement('div');
    sidebarDiv.id = 'sidebar-wrapper';
    sidebarDiv.innerHTML = sidebarHTML;
    
    // Create overlay for mobile
    const overlayDiv = document.createElement('div');
    overlayDiv.id = 'sidebar-overlay';
    
    // Inject at start of wrapper
    wrapper.insertBefore(sidebarDiv, wrapper.firstChild);
    wrapper.appendChild(overlayDiv);

    // 2. Inject Navbar (inside page-content-wrapper)
    const pageContent = document.getElementById('page-content-wrapper');
    if (!pageContent) return;

    const navbarHTML = `
        <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
            <div class="container-fluid">
                <button class="btn btn-outline-success" id="sidebarToggle">
                    <i class="fas fa-bars"></i>
                </button>
                
                <span class="navbar-brand ms-3">
                    ${getPageTitle(activePageId)}
                </span>
                
                <div class="ms-auto d-flex align-items-center">
                   <div class="dropdown">
                        <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle text-dark" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-user-circle fa-lg me-2 text-success"></i>
                            <span id="navUsername">Farmer</span>
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="userDropdown">
                             <li><a class="dropdown-item" href="#">Profile</a></li>
                             <li><hr class="dropdown-divider"></li>
                             <li><a class="dropdown-item text-danger" href="#" onclick="Auth.logout()">Logout</a></li>
                        </ul>
                   </div>
                </div>
            </div>
        </nav>
    `;

    pageContent.insertAdjacentHTML('afterbegin', navbarHTML);

    // 3. Initialize Listeners
    initLayoutListeners();
    
    // 4. Update User Info
    if (window.Auth && typeof Auth.check === 'function') {
         const user = Auth.check();
         if(user && document.getElementById('navUsername')) {
             document.getElementById('navUsername').innerText = user.username;
         }
    }
}

function getPageTitle(id) {
    switch(id) {
        case 'dashboard': return 'Farm Dashboard';
        case 'history': return 'Detection History';
        case 'alerts': return 'System Alerts';
        case 'reports': return 'Download Reports';
        default: return 'AgriGuard';
    }
}

function initLayoutListeners() {
    const wrapper = document.getElementById('wrapper');
    const toggleBtn = document.getElementById('sidebarToggle');
    const closeBtn = document.getElementById('sidebarClose');
    const overlay = document.getElementById('sidebar-overlay');
    
    function toggleSidebar() {
        if (window.innerWidth >= 768) {
             wrapper.classList.toggle('toggled');
        } else {
             wrapper.classList.toggle('mobile-show');
        }
    }
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            toggleSidebar();
        });
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', (e) => {
             e.preventDefault();
             wrapper.classList.remove('mobile-show');
        });
    }
    
    if (overlay) {
        overlay.addEventListener('click', () => {
            wrapper.classList.remove('mobile-show');
        });
    }
}

// Auto-detect page ID based on filename if not provided manually
document.addEventListener("DOMContentLoaded", () => {
    // Only verify auth on protected pages (not login)
    if (!window.location.pathname.includes('login.html')) {
        if (window.Auth) Auth.check(); 
    }
});
