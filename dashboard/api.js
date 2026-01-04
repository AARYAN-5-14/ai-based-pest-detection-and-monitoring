const API_BASE_URL = "http://127.0.0.1:5000";

// Fetch all pest detections
async function fetchAllDetections() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/pests`);
        if (!response.ok) throw new Error("Failed to fetch detections");
        return await response.json();
    } catch (error) {
        console.error("Error fetching detections:", error);
        return [];
    }
}

// Fetch all alerts
async function fetchAllAlerts() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/alerts`);
        if (!response.ok) throw new Error("Failed to fetch alerts");
        return await response.json();
    } catch (error) {
        console.error("Error fetching alerts:", error);
        return [];
    }
}

// Send image for prediction
async function predictPest(imageFile) {
    const formData = new FormData();
    formData.append("image", imageFile);

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Prediction failed");
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
}
