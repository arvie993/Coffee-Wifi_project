# ☕ Coffee & Wifi 💻

A modern Flask web application to help remote workers find the perfect cafe with great coffee, reliable wifi, and available power outlets.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### Core Features
- **📋 Browse Curated Cafes**: View a hand-picked list of cafes with ratings for coffee quality, wifi strength, and power socket availability
- **➕ Add New Cafes**: Contribute new cafes to the community database

### 🆕 New Features
- **🔍 Find Nearby Cafes**: Search for cafes near any city or zip code worldwide using Google Places API
- **📸 Cafe Photos**: View real photos from Google Places for each establishment
- **⭐ Smart Sorting**: Sort results by rating, number of reviews, or alphabetically
- **📍 Live Status**: See if cafes are currently open or closed
- **🗺️ Maps Integration**: Direct links to Google Maps for directions

## 🖼️ Screenshots

### Home Page
Modern dark-themed landing page with clear call-to-action buttons.

### Nearby Cafe Search
Search by city or zip code with beautiful card-based results showing:
- Establishment photos
- Ratings and review counts
- Open/Closed status
- Price level indicators
- Quick links to Google Maps

### Curated Cafe List
Bootstrap table displaying local cafes with emoji ratings:
- ☕ Coffee rating (1-5 cups)
- 💪 Wifi strength (1-5 or ✘ for none)
- 🔌 Power outlets (1-5 or ✘ for none)

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.8+, Flask 2.3.2 |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Forms** | Flask-WTF, WTForms |
| **Styling** | Bootstrap-Flask, Bootstrap Icons |
| **APIs** | Google Places API, Google Geocoding API |
| **Data Storage** | CSV (local), Google Places (search) |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Google Cloud account (for Places API)

### Step 1: Clone the Repository

```bash
git clone https://github.com/arvie993/Coffee-Wifi_project.git
cd Coffee-Wifi_project
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

> ⚠️ **Note for OneDrive users**: If you're syncing via OneDrive, create the venv outside the synced folder to avoid certificate issues:
> ```bash
> python -m venv C:\temp\coffee-wifi-venv
> C:\temp\coffee-wifi-venv\Scripts\Activate.ps1
> ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your keys:
   ```env
   SECRET_KEY=your_secret_key_here
   GOOGLE_PLACES_API_KEY=your_google_api_key_here
   ```

### Step 5: Get Google Places API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Navigate to **APIs & Services** → **Library**
4. Enable these APIs:
   - **Geocoding API**
   - **Places API**
5. Go to **APIs & Services** → **Credentials**
6. Click **Create Credentials** → **API Key**
7. Copy the key to your `.env` file

### Step 6: Run the Application

```bash
python main.py
```

Open your browser and navigate to `http://127.0.0.1:5000`

## 🗺️ Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with navigation |
| `/cafes` | GET | View all curated cafes |
| `/search` | GET, POST | Search for nearby cafes |
| `/add` | GET, POST | Add a new cafe to the database |
| `/api/search` | GET | REST API endpoint for cafe search |

### API Usage

```bash
# Search for cafes near a city
GET /api/search?city=Seattle&radius=5000

# Search by zip code
GET /api/search?zip_code=98052&radius=10000
```

## 📁 Project Structure

```
Coffee-Wifi_project/
├── main.py              # Flask application & routes
├── cafe-data.csv        # Local cafe database
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your environment variables (git-ignored)
├── README.md            # This file
├── ARCHITECTURE.md      # Detailed code documentation
├── static/
│   └── css/
│       └── styles.css   # Custom styling
└── templates/
    ├── base.html        # Base template with navigation
    ├── index.html       # Home page
    ├── cafes.html       # Curated cafe list
    ├── search.html      # Nearby cafe search
    └── add.html         # Add cafe form
```

## 📖 Documentation

For detailed code explanation and architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## 🔧 Configuration Options

### Search Radius Options
- 1 km, 2 km, 5 km (default), 10 km, 25 km

### Sort Options
- ⭐ Highest Rating (default)
- 📝 Most Reviews
- 🔤 Name (A-Z)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Requirements

```
Bootstrap-Flask==2.2.0
Flask==2.3.2
WTForms==3.0.1
Flask-WTF==1.2.1
Werkzeug==3.0.0
python-dotenv==1.0.0
requests==2.31.0
```

## 👤 Author

**Aravind Sridharan**
- GitHub: [@arvie993](https://github.com/arvie993)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Part of the 100 Days of Code Python Bootcamp
- [Bootstrap](https://getbootstrap.com/) for the responsive UI components
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service) for location data
- [Flask](https://flask.palletsprojects.com/) community for excellent documentation

---

<p align="center">Made with ☕ and 💻</p>
