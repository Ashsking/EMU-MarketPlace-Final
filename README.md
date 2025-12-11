 EMU Student Marketplace – Final Project
A full-stack Flask web application designed for the Eastern Mennonite University (EMU) community.
This platform enables student-to-student selling, official EMU store purchasing, secure account management, and personalized dashboards—all built using Python, Flask, SQLAlchemy, and HTML/CSS.
 Overview
The EMU Student Marketplace is a centralized platform where EMU students can buy, sell, and browse items in a safe, EMU-exclusive environment. The platform supports two main item categories:
Student Marketplace Listings – students create and manage their own listings
Official EMU Store Listings – the EMU store can post items for direct purchase
The application includes authentication, item posting and editing, secure order handling, image upload support, and a student dashboard showing purchases, sales, and listings.
Features
 User Authentication
Signup and login (EMU email required)
Secure password hashing
Session-based login state
 Student Marketplace
Create, edit, and delete personal listings
Upload images or use external URLs
Categories & search functionality
Buy student listings with automatic transaction recording
Official EMU Store
Admin-created official merchandise
Stock tracking
Buy Now flow with quantity selection
Automatic order creation
Dashboard
View:
Active listings
Purchases (student marketplace)
Sales (student marketplace)
EMU store orders
 Static Pages
About
Contact
FAQ
Terms
Privacy Policy
📁 Project Structure
EMU-MarketPlace-Final/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── marketplace.html
│   ├── store.html
│   ├── profile.html
│   ├── dashboard.html
│   ├── buy_now.html
│   ├── about.html
│   ├── faq.html
│   ├── terms.html
│   └── privacy.html
│
└── static/
    ├── css/
    ├── js/
    ├── images/
    └── uploads/ (ignored in Git)
 Tech Stack
Backend:
Python
Flask
SQLAlchemy ORM
SQLite
Frontend:
HTML5
CSS3
Jinja2 Templating
Other:
Werkzeug security
Flask-Migrate
 How to Run This Project Locally
1️⃣ Clone the repository
git clone https://github.com/Ashsking/EMU-MarketPlace-Final.git
cd EMU-MarketPlace-Final
2️⃣ Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Initialize the database
flask db upgrade
(or)
python3 app.py   # auto-creates app.db if migrations are ignored
5️⃣ Run the server
flask run
Now visit:
 http://127.0.0.1:5000/
 Future Improvements
Given more time, this platform could be extended with:
Real-time chat between buyers and sellers
Notifications system (email or in-app alerts)
Multiple image uploads per listing
Search filtering improvements
Admin dashboard for official store management
Rating & review system
Payment integration (Stripe / PayPal)
Recommendation algorithms
Mobile-first responsive redesign
 Developer
Ashutosh Niraula
Eastern Mennonite University
Computer Science Major
