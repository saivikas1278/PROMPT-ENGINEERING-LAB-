# Public Transport & Route Assistant

A public transportation route assistant providing comprehensive bus details and visual routing via GraphHopper API and Leaflet Maps.

## 1. Project Structure

```text
public_transport_assistant/
│
├── frontend/
│   ├── templates/         # HTML templates
│   └── static/            # CSS, JS, and other static assets
│
├── backend/
│   ├── app.py             # Main Flask server
│   ├── database.py        # SQLite Database Operations
│   ├── route_service.py   # GraphHopper API Integration
│   ├── requirements.txt   # Python Dependencies
│   ├── .env               # Secret Keys
│   └── transport.db       # SQLite Database
│
├── .gitignore
└── README.md
```

## 2. Backend Setup
The backend runs on **Flask** with an embedded **SQLite database**. It connects to GraphHopper for road routing capabilities.

## 3. Frontend Structure
The frontend utilizes **Jinja2 Templates** coupled with standard HTML, CSS, and some JavaScript to interact with the backend APIs securely. It includes a dynamic Leaflet map to visualize routes computed by GraphHopper.

## 4. Environment Variables
Create a file at `backend/.env` containing:
```env
SECRET_KEY=super_secret_college_key
GRAPHHOPPER_API_KEY=your_key_here
```

## 5. Installation

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment (Windows):
```bash
venv\Scripts\activate
```

Install the required dependencies:
```bash
pip install -r backend/requirements.txt
```

## 6. How to Run the Application
From the root of the project (`public_transport_assistant`), execute:
```bash
python backend/app.py
```
Then navigate to `http://127.0.0.1:5000` in your web browser.

## 7. GraphHopper API Configuration
The `route_service.py` connects to the GraphHopper API for geocoding address strings to coordinates and for generating the physical road path/distance between stops. Ensure `GRAPHHOPPER_API_KEY` is loaded correctly in your `backend/.env`.
