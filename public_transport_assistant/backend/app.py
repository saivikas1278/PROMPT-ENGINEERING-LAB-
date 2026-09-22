from functools import wraps
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, insert_sample_data, get_locations, search_routes, get_route_by_id, get_all_routes, add_route, update_route, delete_route
from route_service import get_graphhopper_route

load_dotenv()

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
CORS(app)
app.secret_key = 'super_secret_college_key'

# Initialize DB on startup
with app.app_context():
    init_db()
    insert_sample_data()

ADMIN_USER = 'admin'
ADMIN_PASS_HASH = generate_password_hash('admin123')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    locations = get_locations()
    return render_template('index.html', locations=locations)

@app.route('/search', methods=['POST'])
def search():
    source = request.form.get('source')
    destination = request.form.get('destination')
    
    if not source or not destination:
        return "Source and destination are required", 400
        
    routes = search_routes(source, destination)
    routes_list = [dict(r) for r in routes]
    route_geometry = None
    
    if routes_list:
        graphhopper_data = get_graphhopper_route(source, destination)
        if graphhopper_data:
            for r in routes_list:
                r["distance"] = graphhopper_data["distance"]
                r["travel_time"] = graphhopper_data["travel_time"]
            import json
            route_geometry = json.dumps(graphhopper_data["path"])
            
    fastest_route = None
    cheapest_route = None
    
    if routes_list:
        fastest_route = min(routes_list, key=lambda r: r["travel_time"])
        cheapest_route = min(routes_list, key=lambda r: r["fare"])
        
        for r in routes_list:
            if r['id'] == fastest_route['id']:
                r['is_fastest'] = True
            if r['id'] == cheapest_route['id']:
                r['is_cheapest'] = True
                
    return render_template('results.html', routes=routes_list, source=source, destination=destination, fastest=fastest_route, cheapest=cheapest_route, route_geometry=route_geometry)

@app.route('/route/<int:route_id>')
def route_details(route_id):
    route = get_route_by_id(route_id)
    if not route:
        return "Route not found", 404
    return render_template('route_details.html', route=route)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password.")
            
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    routes = get_all_routes()
    locations = get_locations()
    return render_template('admin_dashboard.html', total_routes=len(routes), total_locations=len(locations))

@app.route('/admin/routes')
@login_required
def manage_routes():
    routes = get_all_routes()
    return render_template('manage_routes.html', routes=routes)

@app.route('/admin/routes/add', methods=['GET', 'POST'])
@login_required
def add_route_view():
    if request.method == 'POST':
        bus_number = request.form.get('bus_number')
        source = request.form.get('source')
        destination = request.form.get('destination')
        distance = request.form.get('distance')
        travel_time = request.form.get('travel_time')
        fare = request.form.get('fare')
        
        if bus_number and source and destination and distance and travel_time and fare:
            add_route(bus_number, source, destination, float(distance), int(travel_time), float(fare))
            flash("Route added successfully.")
            return redirect(url_for('manage_routes'))
            
    return render_template('add_route.html')

@app.route('/admin/routes/edit/<int:route_id>', methods=['GET', 'POST'])
@login_required
def edit_route_view(route_id):
    route = get_route_by_id(route_id)
    if not route:
        return "Route not found", 404
        
    if request.method == 'POST':
        bus_number = request.form.get('bus_number')
        source = request.form.get('source')
        destination = request.form.get('destination')
        distance = request.form.get('distance')
        travel_time = request.form.get('travel_time')
        fare = request.form.get('fare')
        
        if bus_number and source and destination and distance and travel_time and fare:
            update_route(route_id, bus_number, source, destination, float(distance), int(travel_time), float(fare))
            flash("Route updated successfully.")
            return redirect(url_for('manage_routes'))
            
    return render_template('edit_route.html', route=route)

@app.route('/admin/routes/delete/<int:route_id>', methods=['POST'])
@login_required
def delete_route_view(route_id):
    delete_route(route_id)
    flash("Route deleted successfully.")
    return redirect(url_for('manage_routes'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
