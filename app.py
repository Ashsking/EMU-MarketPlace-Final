import os
from datetime import datetime

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# -------------------------------------------------
# App & config
# -------------------------------------------------
app = Flask(__name__)
app.secret_key = "change-this-secret-key-in-production"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# -------------------------------------------------
# Models
# -------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    listings = db.relationship("Listing", backref="seller", lazy=True, foreign_keys="Listing.seller_id")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(20), nullable=False, default="good")
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500))
    datePosted = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # official_store or student_listing
    listing_type = db.Column(db.String(20), default="student_listing")
    stock_quantity = db.Column(db.Integer, default=1)  # mainly for official store

    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)


class Transaction(db.Model):
    """
    Student-to-student completed purchase.
    One row per completed sale in the student marketplace.
    """
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    price_paid = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    listing = db.relationship("Listing", backref="transactions")
    buyer = db.relationship("User", foreign_keys=[buyer_id], backref="purchases")
    seller = db.relationship("User", foreign_keys=[seller_id], backref="sales")


class Order(db.Model):
    """
    Orders for official EMU store items.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, confirmed, shipped, delivered
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    user = db.relationship("User", backref="orders")
    listing = db.relationship("Listing", backref="orders")


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


@app.context_processor
def inject_user():
    return {"current_user": get_current_user()}


# -------------------------------------------------
# Auth routes
# -------------------------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        error = None

        if not username or not email or not password:
            error = "All fields are required."
        elif not email.endswith("@emu.edu"):
            error = "Please use your EMU email address (@emu.edu)."
        elif User.query.filter_by(username=username).first():
            error = "That username is already taken."
        elif User.query.filter_by(email=email).first():
            error = "That email is already registered."

        if error:
            return render_template("signup.html", error=error)

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        flash(" Welcome to EMU Marketplace! Your account has been created.", "success")
        return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return render_template("login.html", error="Invalid username or password.")

        session["user_id"] = user.id
        flash(f" Welcome back, {user.username}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash(" You've been logged out successfully.", "success")
    return redirect(url_for("index"))


# -------------------------------------------------
# Main pages
# -------------------------------------------------
@app.route("/")
def index():
    """Homepage with featured items from both store and marketplace"""
    # Get latest official store items
    store_items = Listing.query.filter_by(listing_type="official_store") \
        .order_by(Listing.datePosted.desc()) \
        .limit(4).all()

    # Get latest student listings
    student_items = Listing.query.filter_by(listing_type="student_listing") \
        .order_by(Listing.datePosted.desc()) \
        .limit(4).all()

    return render_template("index.html", store_items=store_items, student_items=student_items)


@app.route("/store")
def store():
    """Official EMU Store"""
    category_filter = request.args.get("category", "all")
    search_query = request.args.get("search", "").strip()

    query = Listing.query.filter_by(listing_type="official_store").order_by(Listing.datePosted.desc())

    if category_filter != "all":
        query = query.filter_by(category=category_filter)

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Listing.itemName.ilike(search_pattern),
                Listing.description.ilike(search_pattern)
            )
        )

    listings = query.all()
    return render_template("store.html", listings=listings, category_filter=category_filter, search_query=search_query)


@app.route("/marketplace")
def marketplace():
    """Student-to-Student Marketplace"""
    category_filter = request.args.get("category", "all")
    search_query = request.args.get("search", "").strip()

    query = Listing.query.filter_by(listing_type="student_listing").order_by(Listing.datePosted.desc())

    if category_filter != "all":
        query = query.filter_by(category=category_filter)

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Listing.itemName.ilike(search_pattern),
                Listing.description.ilike(search_pattern)
            )
        )

    listings = query.all()
    return render_template("marketplace.html", listings=listings, category_filter=category_filter, search_query=search_query)


@app.route("/my_orders")
def my_orders():
    """View user's EMU store orders"""
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return render_template("my_orders.html", orders=orders)


# -------------------------------------------------
# Student marketplace: post/edit/delete + buy
# -------------------------------------------------
@app.route("/profile")
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    user_listings = Listing.query.filter_by(
        seller_id=user.id,
        listing_type="student_listing"
    ).order_by(Listing.datePosted.desc()).all()

    return render_template("profile.html", listings=user_listings)


@app.route("/post", methods=["GET", "POST"])
def post():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        item_name = request.form.get("itemName")
        description = request.form.get("description")
        category = request.form.get("category")
        condition = request.form.get("condition")
        price = request.form.get("price")
        image_url = request.form.get("imageUrl", "").strip()

        if not item_name or not description or not category or not condition or not price:
            return render_template("post.html", error="Please fill out all required fields.")

        try:
            price = float(price)
        except ValueError:
            return render_template("post.html", error="Price must be a number.")

        image_path = None
        file = request.files.get("imageFile")

        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(save_path)
                image_path = f"uploads/{filename}"
            else:
                return render_template("post.html", error="Unsupported image type.")
        elif image_url:
            image_path = image_url

        new_item = Listing(
            itemName=item_name,
            description=description,
            category=category,
            condition=condition,
            price=price,
            seller_id=user.id,
            image=image_path,
            listing_type="student_listing"
        )
        db.session.add(new_item)
        db.session.commit()

        flash("Item posted successfully!", "success")
        return redirect(url_for("marketplace"))

    return render_template("post.html")


@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    item = Listing.query.get_or_404(item_id)

    if item.seller_id != user.id:
        return redirect(url_for("profile"))

    if request.method == "POST":
        item.itemName = request.form.get("itemName")
        item.description = request.form.get("description")
        item.category = request.form.get("category")
        item.condition = request.form.get("condition")
        price = request.form.get("price")
        image_url = request.form.get("imageUrl", "").strip()

        try:
            item.price = float(price)
        except (TypeError, ValueError):
            return render_template("edit.html", item=item, error="Price must be numeric.")

        file = request.files.get("imageFile")
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(save_path)
                item.image = f"uploads/{filename}"
        elif image_url:
            item.image = image_url

        db.session.commit()
        flash("Item updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("edit.html", item=item)


@app.route("/delete/<int:item_id>")
def delete(item_id):
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    item = Listing.query.get_or_404(item_id)
    if item.seller_id != user.id:
        return redirect(url_for("profile"))

    db.session.delete(item)
    db.session.commit()
    flash("Item deleted successfully!", "success")
    return redirect(url_for("profile"))


@app.route("/buy_student/<int:listing_id>", methods=["POST"])
def buy_student(listing_id):
    """
    Direct purchase of a student listing at listed price.
    """
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    listing = Listing.query.get_or_404(listing_id)

    if listing.listing_type != "student_listing":
        flash("This item is not a student marketplace listing!", "error")
        return redirect(url_for("store"))

    if listing.seller_id == user.id:
        flash("You cannot buy your own item!", "error")
        return redirect(url_for("marketplace"))

    transaction = Transaction(
        listing_id=listing.id,
        buyer_id=user.id,
        seller_id=listing.seller_id,
        price_paid=listing.price
    )

    # Option: remove listing after it's sold
    db.session.add(transaction)
    db.session.delete(listing)
    db.session.commit()

    flash("Purchase successful! The seller has been recorded in your activity.", "success")
    return redirect(url_for("dashboard"))


# -------------------------------------------------
# Static pages
# -------------------------------------------------
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# -------------------------------------------------
# Dashboard
# -------------------------------------------------
@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    tab = request.args.get("tab", "overview")

    # Listings user currently has up for sale (student marketplace)
    listings = Listing.query.filter_by(
        seller_id=user.id,
        listing_type="student_listing"
    ).all()

    # Student marketplace purchases (you bought from others)
    purchases = Transaction.query.filter_by(buyer_id=user.id).all()

    # Student marketplace sales (others bought from you)
    sales = Transaction.query.filter_by(seller_id=user.id).all()

    # EMU store orders (official merch)
    store_orders = Order.query.filter_by(user_id=user.id).all()

    return render_template(
        "dashboard.html",
        tab=tab,
        listings=listings,
        purchases=purchases,
        sales=sales,
        store_orders=store_orders,
    )

@app.route("/buy/<int:listing_id>", methods=["GET", "POST"])
def buy_now(listing_id):
    user = get_current_user()
    if not user:
        flash("Please login to purchase items.", "error")
        return redirect(url_for("login"))
    
    listing = Listing.query.get_or_404(listing_id)

    if request.method == "POST":
        quantity = int(request.form.get("quantity", 1))

        if quantity > listing.stock_quantity:
            return render_template("buy_now.html", listing=listing, error="Not enough stock available.")

        total = listing.price * quantity

        order = Order(
            user_id=user.id,
            listing_id=listing.id,
            quantity=quantity,
            total_price=total,
            status="confirmed"
        )

        listing.stock_quantity -= quantity
        db.session.add(order)
        db.session.commit()

        return render_template(
            "order_confirmation.html",
            listing=listing,
            quantity=quantity,
            total=total
        )

    return render_template("buy_now.html", listing=listing)


with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)
