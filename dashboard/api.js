const API_BASE_URL = "http://127.0.0.1:5000";

// Fetch all pest detections
async function fetchAllDetections() {
    const response = await fetch(`${API_BASE_URL}/api/pests`);
    return await response.json();
}

// Fetch all alerts
async function fetchAllAlerts() {
    const response = await fetch(`${API_BASE_URL}/api/alerts`);
    return await response.json();
}
