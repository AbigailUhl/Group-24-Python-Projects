# FIFA Player Data Web Application (Django Project)

## Group Members
- [Your Name]
- [Teammate Name]
- [Teammate Name]

## Project Description
This project is a full-stack Django web application that analyzes FIFA player data.  
It allows users to view, create, update, and delete player records, as well as explore analytics based on player performance metrics such as speed, strength, and age.

The application integrates:
- Project 1: FIFA dataset and EDA analysis
- Project 2: API data fetching (weather data)
- Django: Full web interface with CRUD, analytics, and UI

## Dataset & API
- Dataset (Project 1): FIFA Player Dataset (cleaned_players.csv)
- API (Project 2): Weather API (Open-Meteo)


## Application Features

### Core Pages
- Home page (`/`)
- Player list view with pagination (`/records/`)
- Player detail view (`/records/<pk>/`)
- Add player (`/records/add/`)
- Edit player (`/records/<pk>/edit/`)
- Delete player (`/records/<pk>/delete/`)

### Analytics
- Analytics dashboard (`/analytics/`)
- Player distribution by position (bar chart)
- Average speed by club (bar chart)
- Summary statistics table (mean, min, max, etc.)

### API Integration
- Fetch API data (`/fetch/`)
- Django management command: python3 manage.py fetch_data


## Setup Instructions

### 1. Clone the repository
`git clone https://github.com/AbigailUhl/Group-24-Python-Projects'
'cd project3'

### 2. Install dependencies
'pip install -r requirements.txt'

### 3. Run migrations
'python3 manage.py migrate'

### 4. Load intitial dataset
'python3 manage.py seed_data'

### 5. Open browser
'http://127.0.0.1:8000/'

## Screenshots

## Deployment Check
'python3 manage.py check --deploy'
Expected output: System check identified no issues (0 silenced).

## Project Structure
project3/
│── config/
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
│── myapp/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/myapp/
│   ├── static/css/
│   └── management/commands/
│
│── data/raw/
│── requirements.txt
│── README.md






