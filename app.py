# Tourist Place Booking Application
import json
import os
import datetime
from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Data file to persist bookings
DATA_FILE = 'data.json'

# Initial tourist places data
initial_places = {
    "1": {"id": 1, "name": "Taj Mahal, India", "price": 50, "available_slots": 10, "rating": "⭐⭐⭐⭐⭐", "image": "🏛️"},
    "2": {"id": 2, "name": "Eiffel Tower, Paris", "price": 45, "available_slots": 8, "rating": "⭐⭐⭐⭐⭐", "image": "🗼"},
    "3": {"id": 3, "name": "Great Wall, China", "price": 40, "available_slots": 15, "rating": "⭐⭐⭐⭐", "image": "🧱"},
    "4": {"id": 4, "name": "Colosseum, Rome", "price": 35, "available_slots": 12, "rating": "⭐⭐⭐⭐⭐", "image": "🏟️"},
    "5": {"id": 5, "name": "Machu Picchu, Peru", "price": 55, "available_slots": 7, "rating": "⭐⭐⭐⭐", "image": "⛰️"}
}

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            'places': initial_places,
            'bookings': []
        }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TravelEase - Tourist Booking</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .nav {
            background: #f8f9fa;
            padding: 15px;
            display: flex;
            gap: 15px;
            justify-content: center;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .nav button {
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            background: #667eea;
            color: white;
            cursor: pointer;
            border-radius: 8px;
            transition: transform 0.2s;
        }
        
        .nav button:hover {
            transform: translateY(-2px);
            background: #5a67d8;
        }
        
        .content {
            padding: 30px;
            min-height: 500px;
        }
        
        .places-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .place-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 20px;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        
        .place-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border-color: #667eea;
        }
        
        .place-icon {
            font-size: 3em;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .place-name {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .place-details {
            color: #666;
            margin: 10px 0;
        }
        
        .price {
            color: #667eea;
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
        }
        
        .slots {
            text-align: center;
            color: #28a745;
            font-weight: bold;
        }
        
        .rating {
            text-align: center;
            margin: 10px 0;
        }
        
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
            transition: background 0.3s;
        }
        
        .btn:hover {
            background: #5a67d8;
        }
        
        .btn-danger {
            background: #dc3545;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        input, select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .booking-list {
            list-style: none;
        }
        
        .booking-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        @media (max-width: 768px) {
            .places-grid {
                grid-template-columns: 1fr;
            }
            
            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌍 TravelEase</h1>
            <p>Book Your Dream Destination</p>
        </div>
        
        <div class="nav">
            <button onclick="showSection('places')">🏠 View Places</button>
            <button onclick="showSection('bookings')">📋 My Bookings</button>
        </div>
        
        <div class="content">
            <!-- Places Section -->
            <div id="places-section">
                <h2>✨ Available Tourist Places</h2>
                <div class="places-grid">
                    {% for id, place in places.items() %}
                    <div class="place-card" onclick="openBookingModal({{ place.id }})">
                        <div class="place-icon">{{ place.image }}</div>
                        <div class="place-name">{{ place.name }}</div>
                        <div class="price">${{ place.price }}</div>
                        <div class="rating">{{ place.rating }}</div>
                        <div class="slots">✅ Available: {{ place.available_slots }} slots</div>
                        <button class="btn" onclick="event.stopPropagation(); openBookingModal({{ place.id }})">Book Now</button>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Bookings Section -->
            <div id="bookings-section" style="display:none;">
                <h2>📋 My Bookings</h2>
                {% if bookings %}
                    {% for booking in bookings %}
                    <div class="booking-item">
                        <strong>{{ booking.place_name }}</strong><br>
                        Name: {{ booking.visitor_name }}<br>
                        Tickets: {{ booking.tickets }}<br>
                        Date: {{ booking.visit_date }}<br>
                        Total: ${{ booking.total_price }}<br>
                        Booking ID: #{{ booking.id }}
                        <form action="/cancel/{{ booking.id }}" method="POST" style="display:inline;">
                            <button type="submit" class="btn btn-danger" style="margin-top:10px;" onclick="return confirm('Cancel this booking?')">Cancel Booking</button>
                        </form>
                    </div>
                    {% endfor %}
                {% else %}
                    <p>No bookings yet. Start exploring! 🌟</p>
                {% endif %}
            </div>
        </div>
    </div>
    
    <!-- Booking Modal -->
    <div id="booking-modal" class="modal">
        <div class="modal-content">
            <h2>📝 Book Your Ticket</h2>
            <form id="booking-form" action="/book" method="POST">
                <input type="hidden" name="place_id" id="place_id">
                <div class="form-group">
                    <label>Place Name:</label>
                    <input type="text" id="place_name" readonly>
                </div>
                <div class="form-group">
                    <label>Your Name:</label>
                    <input type="text" name="visitor_name" required placeholder="Enter your full name">
                </div>
                <div class="form-group">
                    <label>Number of Tickets:</label>
                    <input type="number" name="tickets" id="tickets" min="1" required onchange="updateTotal()">
                </div>
                <div class="form-group">
                    <label>Visit Date:</label>
                    <input type="date" name="visit_date" required min="{{ today }}">
                </div>
                <div class="form-group">
                    <label>Total Price:</label>
                    <input type="text" id="total_price" readonly>
                </div>
                <button type="submit" class="btn">Confirm Booking</button>
                <button type="button" class="btn" onclick="closeModal()">Cancel</button>
            </form>
        </div>
    </div>
    
    <script>
        let currentPrice = 0;
        
        function showSection(section) {
            if (section === 'places') {
                document.getElementById('places-section').style.display = 'block';
                document.getElementById('bookings-section').style.display = 'none';
            } else {
                document.getElementById('places-section').style.display = 'none';
                document.getElementById('bookings-section').style.display = 'block';
            }
        }
        
        function openBookingModal(placeId) {
            fetch(`/get_place/${placeId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('place_id').value = data.id;
                    document.getElementById('place_name').value = data.name;
                    currentPrice = data.price;
                    document.getElementById('tickets').value = 1;
                    updateTotal();
                    document.getElementById('booking-modal').style.display = 'flex';
                });
        }
        
        function updateTotal() {
            let tickets = document.getElementById('tickets').value;
            let total = currentPrice * tickets;
            document.getElementById('total_price').value = '$' + total;
        }
        
        function closeModal() {
            document.getElementById('booking-modal').style.display = 'none';
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            let modal = document.getElementById('booking-modal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    data = load_data()
    today = datetime.date.today().isoformat()
    return render_template_string(HTML_TEMPLATE, 
                                places=data['places'], 
                                bookings=data['bookings'],
                                today=today)

@app.route('/get_place/<int:place_id>')
def get_place(place_id):
    data = load_data()
    for place in data['places'].values():
        if place['id'] == place_id:
            return jsonify({'id': place['id'], 'name': place['name'], 'price': place['price']})
    return jsonify({'error': 'Place not found'}), 404

@app.route('/book', methods=['POST'])
def book():
    data = load_data()
    place_id = str(request.form.get('place_id'))
    visitor_name = request.form.get('visitor_name')
    tickets = int(request.form.get('tickets'))
    visit_date = request.form.get('visit_date')
    
    if place_id not in data['places']:
        return "Place not found", 404
    
    place = data['places'][place_id]
    
    if place['available_slots'] < tickets:
        return "Not enough slots available", 400
    
    # Update available slots
    place['available_slots'] -= tickets
    
    # Create booking
    booking = {
        'id': len(data['bookings']) + 1001,
        'place_id': place['id'],
        'place_name': place['name'],
        'visitor_name': visitor_name,
        'tickets': tickets,
        'visit_date': visit_date,
        'total_price': place['price'] * tickets
    }
    
    data['bookings'].append(booking)
    save_data(data)
    
    return '''
    <script>
        alert("✅ Booking Confirmed! Booking ID: ''' + str(booking['id']) + '''");
        window.location.href = "/";
    </script>
    '''

@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    data = load_data()
    
    # Find and remove booking
    booking_to_remove = None
    for booking in data['bookings']:
        if booking['id'] == booking_id:
            booking_to_remove = booking
            break
    
    if booking_to_remove:
        # Return slots to the place
        for place in data['places'].values():
            if place['id'] == booking_to_remove['place_id']:
                place['available_slots'] += booking_to_remove['tickets']
                break
        
        data['bookings'].remove(booking_to_remove)
        save_data(data)
    
    return '''
    <script>
        alert("✅ Booking cancelled successfully!");
        window.location.href = "/";
    </script>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
