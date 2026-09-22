const API_BASE_URL = "https://prompt-engineering-lab-0c3z.onrender.com";

let map = null;
let geojsonLayer = null;

document.addEventListener("DOMContentLoaded", () => {
    // 1. Fetch locations for dropdowns
    fetch(`${API_BASE_URL}/api/locations`)
        .then(res => res.json())
        .then(data => {
            const sourceSelect = document.getElementById("source");
            const destSelect = document.getElementById("destination");
            
            sourceSelect.innerHTML = `<option value="" disabled selected>Select Source</option>`;
            destSelect.innerHTML = `<option value="" disabled selected>Select Destination</option>`;
            
            if (data.locations) {
                data.locations.forEach(loc => {
                    const opt1 = document.createElement("option");
                    opt1.value = loc;
                    opt1.textContent = loc;
                    sourceSelect.appendChild(opt1);
                    
                    const opt2 = document.createElement("option");
                    opt2.value = loc;
                    opt2.textContent = loc;
                    destSelect.appendChild(opt2);
                });
            }
        })
        .catch(err => {
            console.error("Error fetching locations:", err);
            document.getElementById("source").innerHTML = `<option value="" disabled selected>Error loading locations</option>`;
            document.getElementById("destination").innerHTML = `<option value="" disabled selected>Error loading locations</option>`;
        });

    // 2. Handle Search Form Submission
    document.getElementById("search-form").addEventListener("submit", (e) => {
        e.preventDefault();
        
        const source = document.getElementById("source").value;
        const destination = document.getElementById("destination").value;
        
        if (!source || !destination) return;
        
        // UI Reset
        document.getElementById("results-container").style.display = "none";
        document.getElementById("error").style.display = "none";
        document.getElementById("loading").style.display = "block";
        document.getElementById("summary-cards").innerHTML = "";
        document.getElementById("route-list").innerHTML = "";
        document.getElementById("map").style.display = "none";
        
        fetch(`${API_BASE_URL}/api/routes?source=${encodeURIComponent(source)}&destination=${encodeURIComponent(destination)}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById("loading").style.display = "none";
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                if (!data.routes || data.routes.length === 0) {
                    throw new Error("No routes found for this journey.");
                }
                
                renderResults(data);
            })
            .catch(err => {
                document.getElementById("loading").style.display = "none";
                document.getElementById("error").style.display = "block";
                document.getElementById("error-message").textContent = err.message;
            });
    });
});

function renderResults(data) {
    document.getElementById("results-container").style.display = "block";
    document.getElementById("results-title").textContent = `Routes from ${data.source} to ${data.destination}`;
    
    // Render Summaries
    const summaryContainer = document.getElementById("summary-cards");
    
    if (data.fastest) {
        summaryContainer.innerHTML += `
            <div class="summary-card fastest">
                <div class="badge">⭐ FASTEST</div>
                <h3>${data.fastest.travel_time} min</h3>
                <p>Bus ${data.fastest.bus_number}</p>
            </div>
        `;
    }
    if (data.cheapest) {
        summaryContainer.innerHTML += `
            <div class="summary-card cheapest">
                <div class="badge">💰 CHEAPEST</div>
                <h3>₹${data.cheapest.fare}</h3>
                <p>Bus ${data.cheapest.bus_number}</p>
            </div>
        `;
    }
    
    // Render Route Cards
    const listContainer = document.getElementById("route-list");
    data.routes.forEach(route => {
        const isFastest = data.fastest && route.id === data.fastest.id;
        const isCheapest = data.cheapest && route.id === data.cheapest.id;
        
        let classes = "route-card";
        if (isFastest) classes += " highlight-fast";
        if (isCheapest) classes += " highlight-cheap";
        
        listContainer.innerHTML += `
            <div class="${classes}">
                <div class="route-info">
                    <div class="bus-number">Bus ${route.bus_number}</div>
                    <div class="route-stats">
                        <span>🛣️ Distance: ${route.distance} km</span>
                        <span>⏱️ Travel Time: ${route.travel_time} minutes</span>
                        <span>💵 Fare: ₹${route.fare}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    // Render Map if Geometry is available
    if (data.route_geometry) {
        document.getElementById("map").style.display = "block";
        
        if (!map) {
            map = L.map('map');
            // Adding a default tile layer (OpenStreetMap)
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '© OpenStreetMap'
            }).addTo(map);
        }
        
        if (geojsonLayer) {
            map.removeLayer(geojsonLayer);
        }
        
        let geoJsonData = data.route_geometry;
        if (typeof geoJsonData === 'string') {
            geoJsonData = JSON.parse(geoJsonData);
        }
        
        geojsonLayer = L.geoJSON(geoJsonData, {
            style: function (feature) {
                return {color: "#007BFF", weight: 5, opacity: 0.8};
            }
        }).addTo(map);
        
        map.fitBounds(geojsonLayer.getBounds());
    }
}
