# ☕ Coffee & Wifi 💻

A Flask web application to help you find cafes with great coffee, reliable wifi, and available power outlets for remote work.

## Features

- **Browse Cafes**: View a list of cafes with ratings for coffee quality, wifi strength, and power socket availability
- **Add New Cafes**: Secret `/add` route to contribute new cafes to the database
- **Google Maps Integration**: Direct links to cafe locations on Google Maps
- **Responsive Design**: Built with Bootstrap 5 for a clean, mobile-friendly interface

## Screenshots

### Home Page
The landing page with a dark theme and call-to-action button.

### Cafes List
A Bootstrap table displaying all cafes with their ratings using emoji indicators:
- ☕ Coffee rating (1-5 cups)
- 💪 Wifi strength (1-5 or ✘ for none)
- 🔌 Power outlets (1-5 or ✘ for none)

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap 5
- **Forms**: Flask-WTF, WTForms
- **Styling**: Bootstrap-Flask
- **Data Storage**: CSV file

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/arvie993/Coffee-Wifi_project.git
   cd Coffee-Wifi_project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python main.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000`

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/cafes` | View all cafes |
| `/add` | Add a new cafe (secret route) |

## Project Structure

```
Coffee-Wifi_project/
├── main.py              # Flask application
├── cafe-data.csv        # Cafe database
├── requirements.txt     # Python dependencies
├── static/
│   └── css/
│       └── styles.css   # Custom styling
└── templates/
    ├── base.html        # Base template
    ├── index.html       # Home page
    ├── cafes.html       # Cafes list
    └── add.html         # Add cafe form
```

## Requirements

- Python 3.8+
- Flask 2.3.2
- Flask-WTF 1.2.1
- WTForms 3.0.1
- Bootstrap-Flask 2.2.0
- Werkzeug 3.0.0

## Author

**Arvie Sridharan**
- GitHub: [@arvie993](https://github.com/arvie993)

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Part of the 100 Days of Code Python Bootcamp
- Bootstrap for the responsive UI components
- Flask community for excellent documentation
