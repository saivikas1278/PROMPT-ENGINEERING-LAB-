# Public Transport & Route Assistant

## 🎓 Project Objective
The **Public Transport & Route Assistant** is a simple, responsive web-based application built for a college project (Team 13 - Transportation & Mobility). It helps commuters find available transport routes between a source and a destination. The system accurately displays the fastest and cheapest route options without relying on external APIs, machine learning, or complex architectures.

## ✨ Features
### For Passengers (Users):
- Search for available transport routes by selecting a Source and Destination.
- Compare available bus routes by travel time, distance, and fare.
- Automatically identifies and highlights the **Fastest Route** (⭐) and **Cheapest Route** (💰).
- View detailed breakdown of specific routes, including stops.

### For Administrators:
- Secure login portal using hashed credentials.
- Dashboard with high-level statistics (total routes, total locations).
- Complete CRUD (Create, Read, Update, Delete) management interface for the bus routes.

## 🛠️ Technology Stack
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript (Vanilla)
- **Backend:** Python 3, Flask
- **Database:** SQLite3

## 💻 System Requirements
- Python 3.8 or higher
- Modern web browser (Chrome, Edge, Firefox, Safari)

## 🚀 Installation Steps
Open a terminal and follow these steps to set up the project locally.

1. **Clone or extract the project directory.**
2. **Navigate into the project directory:**
   ```bash
   cd public_transport_assistant
   ```
3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
4. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```
5. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ How to Run
Once the environment is set up and activated, simply start the application:

```bash
python app.py
```

Then, open your web browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔐 Admin Credentials
For college demonstration purposes, the system is seeded with a default administrator account.

- **Username:** `admin`
- **Password:** `admin123`

*(Note: The password is securely hashed in the codebase using `werkzeug.security`)*

## 🗄️ Database Information
The application utilizes a local SQLite database (`transport.db`). 
- On the very first run, the system automatically builds the database schema and populates the `routes` table with 10 realistic sample records covering local areas like SRKR Engineering College, Bhimavaram Bus Stand, Eluru, etc.
- No database server setup is required.

## 📁 Project Structure
```text
public_transport_assistant/
│
├── app.py                   # Main Flask application and routing
├── database.py              # SQLite logic and CRUD operations
├── transport.db             # Auto-generated SQLite database file
├── requirements.txt         # Project dependencies (Flask)
├── README.md                # Project documentation
│
├── templates/               # HTML Views (Jinja2)
│   ├── base.html            # Foundation layout
│   ├── index.html           # Passenger search page
│   ├── results.html         # Route search results
│   ├── route_details.html   # Detailed bus view
│   ├── admin_login.html     # Secure login
│   ├── admin_dashboard.html # Admin panel home
│   ├── add_route.html       # Create form
│   ├── edit_route.html      # Update form
│   └── manage_routes.html   # CRUD table view
│
└── static/
    └── css/
        └── style.css        # Custom CSS styling (No frameworks)
```

## 📸 Sample Screenshots
*(Add your screenshots here before final submission)*
- `home_search.png`: User selecting locations.
- `search_results.png`: Cards showing the cheapest and fastest bus.
- `admin_dashboard.png`: The admin managing records.

## 🔮 Future Enhancements
- Integration with external mapping systems (e.g., OpenStreetMap) for live route visualization.
- User account creation and ticket booking functionalities.
- Implement live bus GPS tracking and real-time traffic updates.
