#  EMU Student Marketplace – Final Project

A full-stack Flask web application designed for the Eastern Mennonite University (EMU) community.  
This platform enables student-to-student selling, official EMU store purchasing, secure account management, and personalized dashboards — all built using Python, Flask, SQLAlchemy, and HTML/CSS.

---

##  Overview

The EMU Student Marketplace is a centralized platform where EMU students can buy, sell, and browse items in a safe, EMU-exclusive environment. The platform supports two main item categories:

- **Student Marketplace Listings** – students create and manage their own listings  
- **Official EMU Store Listings** – the EMU store can post items for direct purchase  

The application includes authentication, image upload support, item posting/editing, secure order handling, and a student dashboard showing purchases, sales, and listings.

---

##  Features

###  User Authentication
- Signup and login (EMU email required)  
- Secure password hashing  
- Session-based login state  

###  Student Marketplace
- Create, edit, and delete personal listings  
- Upload images or use external URLs  
- Category filters + full search  
- Buy student listings with automatic transaction recording  

###  Official EMU Store
- Admin-created store merchandise  
- Stock tracking  
- Buy Now checkout with quantity selection  
- Auto-generated order records  

###  Dashboard
- Active listings  
- Purchases  
- Sales  
- EMU store orders  

###  Static Pages
- About  
- FAQ  
- Terms  
- Privacy Policy  

---

## Project Structure

EMU-MarketPlace-Final/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── signup.html
│ ├── login.html
│ ├── marketplace.html
│ ├── store.html
│ ├── profile.html
│ ├── dashboard.html
│ ├── buy_now.html
│ ├── terms.html
│ ├── faq.html
│ └── privacy.html
│
└── static/
├── css/
├── js/
├── images/
└── uploads/ (ignored in Git)

---

##  Tech Stack

**Backend:** Python, Flask, SQLAlchemy, SQLite  
**Frontend:** HTML, CSS, Jinja2 Templates  
**Other:** Werkzeug Security, Flask-Migrate  

---

##  How to Run

### 1. Clone Repo
```bash
git clone https://github.com/Ashsking/EMU-MarketPlace-Final.git
cd EMU-MarketPlace-Final
2. Create & Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Run the App
flask run
Then open: http://127.0.0.1:5000/

 Future Improvements
Real-time chat
Notifications system
More advanced search filters
Multi-image support
Full admin dashboard
Rating and review system
Payment processing (Stripe/PayPal)

 Developer
Ashutosh Niraula
Eastern Mennonite University — Computer Science
