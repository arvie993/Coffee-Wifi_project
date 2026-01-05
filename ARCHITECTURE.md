# ☕ Coffee & Wifi - Architecture & Code Explanation

This document provides a detailed explanation of the Coffee & Wifi application's architecture, code structure, and implementation details.

## Table of Contents

1. [Overview](#overview)
2. [Application Architecture](#application-architecture)
3. [Backend Components](#backend-components)
4. [Frontend Components](#frontend-components)
5. [API Integration](#api-integration)
6. [Data Flow](#data-flow)
7. [Key Features Implementation](#key-features-implementation)

---

## Overview

Coffee & Wifi is a Flask-based web application that helps remote workers find cafes with good wifi, power outlets, and quality coffee. The application combines a local database of curated cafes with real-time search capabilities powered by Google Places API.

### Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.8+, Flask 2.3.2 |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Forms | Flask-WTF, WTForms |
| Templating | Jinja2 |
| API Integration | Google Places API, Google Geocoding API |
| Data Storage | CSV (local cafes), Google Places (nearby search) |

---

## Application Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                           │
├─────────────────────────────────────────────────────────────────┤
│                              │                                   │
│    ┌─────────────────────────▼─────────────────────────┐        │
│    │              Flask Application                      │        │
│    │  ┌─────────────────────────────────────────────┐   │        │
│    │  │              Routes (main.py)                │   │        │
│    │  │  • /           → Home page                   │   │        │
│    │  │  • /cafes      → Local cafe list             │   │        │
│    │  │  • /search     → Nearby cafe search          │   │        │
│    │  │  • /add        → Add new cafe                │   │        │
│    │  │  • /api/search → REST API endpoint           │   │        │
│    │  └─────────────────────────────────────────────┘   │        │
│    │                        │                            │        │
│    │  ┌─────────────────────▼─────────────────────────┐ │        │
│    │  │              Forms (WTForms)                   │ │        │
│    │  │  • CafeForm        → Add cafe form            │ │        │
│    │  │  • LocationSearchForm → Search form           │ │        │
│    │  └─────────────────────────────────────────────┘  │        │
│    │                        │                            │        │
│    │  ┌─────────────────────▼─────────────────────────┐ │        │
│    │  │           Templates (Jinja2)                   │ │        │
│    │  │  • base.html    → Navigation & layout         │ │        │
│    │  │  • index.html   → Landing page                │ │        │
│    │  │  • cafes.html   → Cafe list table             │ │        │
│    │  │  • search.html  → Search interface            │ │        │
│    │  │  • add.html     → Add cafe form               │ │        │
│    │  └─────────────────────────────────────────────┘  │        │
│    └─────────────────────────────────────────────────────┘       │
│                              │                                   │
│              ┌───────────────┴───────────────┐                   │
│              ▼                               ▼                   │
│    ┌─────────────────┐             ┌─────────────────┐          │
│    │  cafe-data.csv  │             │ Google Places   │          │
│    │  (Local Store)  │             │     API         │          │
│    └─────────────────┘             └─────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Backend Components

### main.py - Core Application

The main application file contains all routes, forms, and business logic.

#### 1. Application Setup

```python
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', '')
```

**Key Points:**
- `load_dotenv()` loads sensitive configuration from `.env` file
- `Bootstrap5(app)` integrates Bootstrap 5 styling
- API keys are stored securely in environment variables

#### 2. Form Classes

**CafeForm** - For adding new cafes to the local database:

```python
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[...])
    wifi_rating = SelectField('Wifi Strength Rating', choices=[...])
    power_rating = SelectField('Power Socket Availability', choices=[...])
    submit = SubmitField('Submit')
```

**LocationSearchForm** - For searching nearby cafes:

```python
class LocationSearchForm(FlaskForm):
    city = StringField('City Name', validators=[Optional()])
    zip_code = StringField('Zip/Postal Code', validators=[Optional()])
    radius = SelectField('Search Radius', choices=[
        ('1000', '1 km'), ('2000', '2 km'), ('5000', '5 km'),
        ('10000', '10 km'), ('25000', '25 km')
    ], default='5000')
    sort_by = SelectField('Sort By', choices=[
        ('rating', '⭐ Highest Rating'),
        ('reviews', '📝 Most Reviews'),
        ('name', '🔤 Name (A-Z)')
    ], default='rating')
    submit = SubmitField('Search Nearby Cafes')
```

#### 3. Google Places API Integration

**Geocoding Function** - Converts location names to coordinates:

```python
def get_coordinates_from_location(city=None, zip_code=None):
    """Convert city or zip code to lat/lng coordinates"""
    query = zip_code if zip_code else city
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': query,
        'key': GOOGLE_PLACES_API_KEY
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None
```

**Nearby Search Function** - Finds cafes near coordinates:

```python
def search_nearby_cafes(lat, lng, radius=5000):
    """Search for nearby cafes using Google Places API"""
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{lng}",
        'radius': radius,
        'type': 'cafe',
        'key': GOOGLE_PLACES_API_KEY
    }
    response = requests.get(places_url, params=params)
    data = response.json()
    
    cafes = []
    for place in data['results'][:20]:
        # Extract photo URL if available
        photo_url = None
        if place.get('photos'):
            photo_ref = place['photos'][0].get('photo_reference')
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={GOOGLE_PLACES_API_KEY}"
        
        cafe = {
            'name': place.get('name'),
            'address': place.get('vicinity'),
            'rating': place.get('rating', 'N/A'),
            'user_ratings_total': place.get('user_ratings_total', 0),
            'place_id': place.get('place_id'),
            'open_now': place.get('opening_hours', {}).get('open_now'),
            'price_level': place.get('price_level'),
            'photo_url': photo_url,
            'lat': place['geometry']['location']['lat'],
            'lng': place['geometry']['location']['lng']
        }
        cafes.append(cafe)
    return cafes
```

#### 4. Route Handlers

**Search Route with Sorting:**

```python
@app.route('/search', methods=['GET', 'POST'])
def search_cafes():
    form = LocationSearchForm()
    nearby_cafes = []
    
    if form.validate_on_submit():
        lat, lng = get_coordinates_from_location(
            city=form.city.data, 
            zip_code=form.zip_code.data
        )
        
        if lat and lng:
            nearby_cafes = search_nearby_cafes(lat, lng, int(form.radius.data))
            
            # Sort results based on user selection
            sort_by = form.sort_by.data
            if sort_by == 'rating':
                nearby_cafes.sort(key=lambda x: x['rating'] or 0, reverse=True)
            elif sort_by == 'reviews':
                nearby_cafes.sort(key=lambda x: x['user_ratings_total'], reverse=True)
            elif sort_by == 'name':
                nearby_cafes.sort(key=lambda x: x['name'].lower())
    
    return render_template('search.html', form=form, cafes=nearby_cafes)
```

---

## Frontend Components

### Template Hierarchy

```
base.html (Layout)
    ├── index.html (Home)
    ├── cafes.html (Local Cafes)
    ├── search.html (Nearby Search)
    └── add.html (Add Cafe Form)
```

### base.html - Navigation & Layout

The base template provides:
- Responsive navigation bar with Bootstrap 5
- Bootstrap Icons integration
- Common CSS and JavaScript includes

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="{{ url_for('home') }}">☕ Coffee & Wifi</a>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('home') }}">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('cafes') }}">Our Cafes</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('search_cafes') }}">Find Nearby</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

### search.html - Modern Card Design

The search results use a modern card-based design with:
- Gradient backgrounds
- Photo integration from Google Places
- Status badges (Open/Closed)
- Rating overlays
- Action buttons for Maps/Directions

```html
<div class="card h-100 border-0 shadow-lg" 
     style="border-radius: 16px; background: linear-gradient(145deg, #1a1a2e, #16213e);">
    
    <!-- Photo with overlay badges -->
    <div class="position-relative">
        <img src="{{ cafe.photo_url }}" class="card-img-top" style="height: 180px; object-fit: cover;">
        
        <!-- Open/Closed badge -->
        <div class="position-absolute top-0 end-0 m-2">
            {% if cafe.open_now %}
            <span class="badge rounded-pill" style="background: linear-gradient(135deg, #11998e, #38ef7d);">
                Open Now
            </span>
            {% endif %}
        </div>
        
        <!-- Rating badge -->
        <div class="position-absolute bottom-0 start-0 m-2">
            <span class="badge" style="background: rgba(0,0,0,0.7); backdrop-filter: blur(10px);">
                ⭐ {{ cafe.rating }}
            </span>
        </div>
    </div>
    
    <!-- Card content -->
    <div class="card-body">
        <h5 class="card-title text-white">{{ cafe.name }}</h5>
        <p class="text-white-50">{{ cafe.address }}</p>
    </div>
</div>
```

---

## API Integration

### Google APIs Used

1. **Geocoding API**
   - Converts addresses/zip codes to coordinates
   - Endpoint: `https://maps.googleapis.com/maps/api/geocode/json`

2. **Places API - Nearby Search**
   - Finds cafes within a radius of coordinates
   - Endpoint: `https://maps.googleapis.com/maps/api/place/nearbysearch/json`

3. **Places API - Photos**
   - Retrieves establishment photos
   - Endpoint: `https://maps.googleapis.com/maps/api/place/photo`

### API Response Handling

```python
# Example Places API response structure
{
    "results": [
        {
            "name": "Starbucks",
            "vicinity": "123 Main St, City",
            "rating": 4.2,
            "user_ratings_total": 582,
            "opening_hours": {"open_now": true},
            "price_level": 2,
            "photos": [{"photo_reference": "..."}],
            "geometry": {"location": {"lat": 40.123, "lng": -74.456}},
            "place_id": "ChIJ..."
        }
    ],
    "status": "OK"
}
```

---

## Data Flow

### Search Flow

```
User Input (City/Zip)
        │
        ▼
┌───────────────────┐
│  Form Validation  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Geocoding API    │ → Convert to Lat/Lng
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Places Nearby API │ → Get cafe list
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Sort Results     │ → By rating/reviews/name
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Render Template  │ → Display cards
└───────────────────┘
```

### Add Cafe Flow

```
User Input (Form)
        │
        ▼
┌───────────────────┐
│  Form Validation  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Write to CSV     │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Redirect to /cafes│
└───────────────────┘
```

---

## Key Features Implementation

### 1. Responsive Navigation

Uses Bootstrap 5's responsive navbar with collapsible menu for mobile devices.

### 2. Modern Card Design

- CSS gradients for dark theme
- `backdrop-filter: blur()` for glassmorphism effects
- `object-fit: cover` for consistent image sizing
- Bootstrap Icons for visual enhancement

### 3. Sorting Algorithm

```python
# Rating sort (handles 'N/A' values)
cafes.sort(key=lambda x: x['rating'] if x['rating'] != 'N/A' else 0, reverse=True)

# Review count sort
cafes.sort(key=lambda x: x['user_ratings_total'], reverse=True)

# Alphabetical sort (case-insensitive)
cafes.sort(key=lambda x: x['name'].lower())
```

### 4. Error Handling

- API key validation before making requests
- Location not found handling
- Empty results messaging
- Certificate error workaround for OneDrive environments

### 5. Security Best Practices

- Environment variables for sensitive data
- CSRF protection via Flask-WTF
- Input validation with WTForms validators

---

## Environment Setup

### Required Environment Variables

```env
SECRET_KEY=your_secret_key_here
GOOGLE_PLACES_API_KEY=your_google_api_key_here
```

### Google Cloud Setup

1. Create a project at [Google Cloud Console](https://console.cloud.google.com/)
2. Enable APIs:
   - Geocoding API
   - Places API
3. Create credentials (API Key)
4. (Optional) Restrict API key to specific APIs and HTTP referrers

---

## Future Enhancements

Potential improvements for the application:

1. **Database Migration**: Move from CSV to SQLite/PostgreSQL
2. **User Authentication**: Allow users to save favorite cafes
3. **Reviews System**: Let users add reviews to local cafes
4. **Map View**: Display results on an interactive map
5. **Caching**: Cache API results to reduce API calls
6. **PWA Support**: Make the app installable on mobile devices

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

*Documentation last updated: January 2026*
