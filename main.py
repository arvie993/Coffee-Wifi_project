from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL, Optional
from dotenv import load_dotenv
import csv
import os
import requests
import ssl

# Fix for OneDrive certificate blocking - use Windows certificate store
try:
    import certifi
    # Try to use Windows certificate store via pip-system-certs or ssl
    import ssl
    ssl_context = ssl.create_default_context()
    # This will use the Windows system certificate store
except:
    pass

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

# Google Places API Key (add to .env file)
GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', '')


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[
        ('✘', '✘'),
        ('☕', '☕'),
        ('☕☕', '☕☕'),
        ('☕☕☕', '☕☕☕'),
        ('☕☕☕☕', '☕☕☕☕'),
        ('☕☕☕☕☕', '☕☕☕☕☕')
    ], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating', choices=[
        ('✘', '✘'),
        ('💪', '💪'),
        ('💪💪', '💪💪'),
        ('💪💪💪', '💪💪💪'),
        ('💪💪💪💪', '💪💪💪💪'),
        ('💪💪💪💪💪', '💪💪💪💪💪')
    ], validators=[DataRequired()])
    power_rating = SelectField('Power Socket Availability', choices=[
        ('✘', '✘'),
        ('🔌', '🔌'),
        ('🔌🔌', '🔌🔌'),
        ('🔌🔌🔌', '🔌🔌🔌'),
        ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
        ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')


class LocationSearchForm(FlaskForm):
    """Form for searching cafes by location"""
    city = StringField('City Name', validators=[Optional()])
    zip_code = StringField('Zip/Postal Code', validators=[Optional()])
    radius = SelectField('Search Radius', choices=[
        ('1000', '1 km'),
        ('2000', '2 km'),
        ('5000', '5 km'),
        ('10000', '10 km'),
        ('25000', '25 km')
    ], default='5000')
    sort_by = SelectField('Sort By', choices=[
        ('rating', '⭐ Highest Rating'),
        ('reviews', '📝 Most Reviews'),
        ('name', '🔤 Name (A-Z)')
    ], default='rating')
    submit = SubmitField('Search Nearby Cafes')


def get_coordinates_from_location(city=None, zip_code=None):
    """Convert city or zip code to lat/lng coordinates using Google Geocoding API"""
    if not GOOGLE_PLACES_API_KEY:
        return None, None
    
    query = zip_code if zip_code else city
    if not query:
        return None, None
    
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': query,
        'key': GOOGLE_PLACES_API_KEY
    }
    
    try:
        response = requests.get(geocode_url, params=params)
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    return None, None


def search_nearby_cafes(lat, lng, radius=5000):
    """Search for nearby cafes using Google Places API"""
    if not GOOGLE_PLACES_API_KEY:
        return []
    
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{lng}",
        'radius': radius,
        'type': 'cafe',
        'key': GOOGLE_PLACES_API_KEY
    }
    
    try:
        response = requests.get(places_url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            cafes = []
            for place in data['results'][:20]:  # Limit to 20 results
                # Get photo URL if available
                photo_url = None
                if place.get('photos'):
                    photo_ref = place['photos'][0].get('photo_reference')
                    if photo_ref:
                        photo_url = (
                            f"https://maps.googleapis.com/maps/api/place/photo"
                            f"?maxwidth=400&photo_reference={photo_ref}"
                            f"&key={GOOGLE_PLACES_API_KEY}"
                        )
                
                cafe = {
                    'name': place.get('name', 'Unknown'),
                    'address': place.get('vicinity', 'Address not available'),
                    'rating': place.get('rating', 'N/A'),
                    'user_ratings_total': place.get('user_ratings_total', 0),
                    'place_id': place.get('place_id', ''),
                    'open_now': place.get('opening_hours', {}).get('open_now', 'Unknown'),
                    'price_level': place.get('price_level'),  # None if not available
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng'],
                    'photo_url': photo_url
                }
                cafes.append(cafe)
            return cafes
    except Exception as e:
        print(f"Places API error: {e}")
    
    return []


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open_time.data},"
                           f"{form.close_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


@app.route('/search', methods=['GET', 'POST'])
def search_cafes():
    """Search for nearby cafes by city or zip code"""
    form = LocationSearchForm()
    nearby_cafes = []
    search_location = None
    error_message = None
    
    if form.validate_on_submit():
        city = form.city.data
        zip_code = form.zip_code.data
        radius = int(form.radius.data)
        sort_by = form.sort_by.data
        
        if not city and not zip_code:
            error_message = "Please enter either a city name or zip code."
        elif not GOOGLE_PLACES_API_KEY:
            error_message = "Google Places API key not configured. Please add GOOGLE_PLACES_API_KEY to your .env file."
        else:
            lat, lng = get_coordinates_from_location(city=city, zip_code=zip_code)
            
            if lat and lng:
                search_location = city if city else zip_code
                nearby_cafes = search_nearby_cafes(lat, lng, radius)
                
                # Sort results based on user selection
                if nearby_cafes:
                    if sort_by == 'rating':
                        nearby_cafes.sort(
                            key=lambda x: (x['rating'] if x['rating'] != 'N/A' else 0),
                            reverse=True
                        )
                    elif sort_by == 'reviews':
                        nearby_cafes.sort(
                            key=lambda x: x['user_ratings_total'],
                            reverse=True
                        )
                    elif sort_by == 'name':
                        nearby_cafes.sort(key=lambda x: x['name'].lower())
                
                if not nearby_cafes:
                    error_message = f"No cafes found near {search_location}. Try increasing the search radius."
            else:
                error_message = f"Could not find location: {city or zip_code}. Please check your input."
    
    return render_template('search.html', 
                         form=form, 
                         cafes=nearby_cafes, 
                         location=search_location,
                         error=error_message)


@app.route('/api/search')
def api_search_cafes():
    """API endpoint for searching cafes (for AJAX requests)"""
    city = request.args.get('city', '')
    zip_code = request.args.get('zip_code', '')
    radius = request.args.get('radius', 5000, type=int)
    
    if not city and not zip_code:
        return jsonify({'error': 'Please provide city or zip_code parameter'}), 400
    
    if not GOOGLE_PLACES_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    lat, lng = get_coordinates_from_location(city=city, zip_code=zip_code)
    
    if not lat or not lng:
        return jsonify({'error': 'Location not found'}), 404
    
    cafes = search_nearby_cafes(lat, lng, radius)
    return jsonify({
        'location': city or zip_code,
        'count': len(cafes),
        'cafes': cafes
    })


if __name__ == '__main__':
    app.run(debug=True)
