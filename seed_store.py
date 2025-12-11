from app import db, Listing, app

items = [
    # ---- TEXTBOOKS ----
    {
        "itemName": "Chemistry Textbook",
        "description": "EMU-approved chemistry textbook.",
        "category": "textbooks",
        "price": 89.99,
        "image": "images/store/chemistry_book.png",
        "listing_type": "official_store",
        "stock_quantity": 10
    },
    {
        "itemName": "Physics Textbook",
        "description": "EMU physics textbook, latest edition.",
        "category": "textbooks",
        "price": 94.99,
        "image": "images/store/physics_book.png",
        "listing_type": "official_store",
        "stock_quantity": 10
    },
    {
        "itemName": "Nursing Book",
        "description": "Required nursing program textbook.",
        "category": "textbooks",
        "price": 129.99,
        "image": "images/store/nursing_book.png",
        "listing_type": "official_store",
        "stock_quantity": 10
    },

    # ---- CLOTHING ----
    {
        "itemName": "EMU Hoodie (Blue)",
        "description": "Blue Eastern Mennonite University hoodie.",
        "category": "clothing",
        "price": 49.99,
        "image": "images/store/hoodie_blue.png",
        "listing_type": "official_store",
        "stock_quantity": 15
    },
    {
        "itemName": "EMU Hoodie (White)",
        "description": "White EMU hoodie with embroidered logo.",
        "category": "clothing",
        "price": 49.99,
        "image": "images/store/hoodie_white.png",
        "listing_type": "official_store",
        "stock_quantity": 15
    },
    {
        "itemName": "EMU Sweatshirt",
        "description": "Classic EMU sweatshirt.",
        "category": "clothing",
        "price": 39.99,
        "image": "images/store/emu_sweatshirt.png",
        "listing_type": "official_store",
        "stock_quantity": 20
    },
    {
        "itemName": "EMU Jersey",
        "description": "EMU athletic jersey.",
        "category": "clothing",
        "price": 59.99,
        "image": "images/store/emu_jersey.png",
        "listing_type": "official_store",
        "stock_quantity": 20
    },
    {
        "itemName": "EMU Hat",
        "description": "EMU baseball-style hat.",
        "category": "clothing",
        "price": 19.99,
        "image": "images/store/emu_hat.png",
        "listing_type": "official_store",
        "stock_quantity": 30
    },

    # ---- DORM ITEMS ----
    {
        "itemName": "Dorm Lamp",
        "description": "LED desk lamp perfect for EMU dorms.",
        "category": "dorm",
        "price": 24.99,
        "image": "images/store/lamp.png",
        "listing_type": "official_store",
        "stock_quantity": 25
    },
    {
        "itemName": "Dorm Mattress Topper",
        "description": "Comfy mattress topper for better sleep.",
        "category": "dorm",
        "price": 89.99,
        "image": "images/store/mattress.png",
        "listing_type": "official_store",
        "stock_quantity": 20
    },
    {
        "itemName": "EMU Pillow",
        "description": "Soft pillow with EMU branding.",
        "category": "dorm",
        "price": 29.99,
        "image": "images/store/pillow.png",
        "listing_type": "official_store",
        "stock_quantity": 40
    },
]

# ---------------------------
# FIX: Wrap in app context
# ---------------------------
with app.app_context():
    for item in items:
        db.session.add(Listing(**item))

    db.session.commit()
    print("🎉 Store items added!")
