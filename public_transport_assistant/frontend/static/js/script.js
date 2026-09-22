const API_BASE_URL = "https://prompt-engineering-lab-0c3z.onrender.com";

/**
 * Example function to manually fetch routes.
 * The current application uses SSR (Server-Side Rendering) with HTML forms, 
 * but this is how you would call the backend via JS if transitioning to a SPA.
 */
function fetchRoutes(source, destination) {
    const formData = new URLSearchParams();
    formData.append('source', source);
    formData.append('destination', destination);

    fetch(`${API_BASE_URL}/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
    })
    .then(response => response.text())
    .then(html => {
        console.log("Response received from backend.");
        // If this was an SPA, you'd inject the HTML or parse JSON here.
    })
    .catch(error => {
        console.error("Error communicating with backend:", error);
    });
}
