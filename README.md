# EMU Student Marketplace

A Flask web application for EMU students to buy and sell items on campus - like Facebook Marketplace but specifically for the EMU community.

## Features
-  User authentication (signup/login with secure password hashing)
-  Post items for sale with image uploads or URLs
-  Category filtering (Textbooks, Clothing, Dorm items, Other)
-  Edit and delete your own listings
-  View seller contact information when logged in
-  SQLite database for persistent data storage

## Technologies Used
- **Backend:** Flask, SQLAlchemy, Flask-Migrate
- **Frontend:** HTML, Jinja2 templating, Pico CSS
- **Database:** SQLite
- **Security:** Werkzeug password hashing, Flask sessions

## Installation & Setup

1. Clone this repository:
```bash
git clone https://github.com/YOUR-USERNAME/EMU-Student-Marketplace.git
cd EMU-Student-Marketplace
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

5. Run the application:
```bash
python app.py
```

6. Open your browser to `http://localhost:5000`

## Project Structure
```
EMU-Student-Marketplace/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Marketplace homepage
│   ├── login.html        # Login page
│   ├── signup.html       # Signup page
│   ├── post.html         # Post new item
│   ├── edit.html         # Edit item
│   └── profile.html      # User profile/listings
├── static/               # Static files
│   ├── pico.min.css     # Pico CSS framework
│   └── uploads/         # Uploaded images
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Assignment Requirements Met
 **GET route with iterable data:** Homepage displays all listings from database  
 **POST route accepting form data:** Multiple forms (signup, login, post item, edit)  
 **Base template inheritance:** All pages extend `base.html` with Pico CSS and navbar  
 **Working forms:** Signup, login, post item, and edit item forms all functional  
 **Database integration:** SQLite with User and Listing models and relationships  
 **User authentication:** Secure login/logout with password hashing  

## Database Schema

**User Model:**
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- listings (Relationship to Listing model)

**Listing Model:**
- id (Primary Key)
- itemName
- description
- category
- price
- image
- datePosted
- seller_id (Foreign Key to User)

## Future Enhancements
- Search functionality
- Item detail pages
- User ratings/reviews
- Messaging system between buyers and sellers
- Image optimization
