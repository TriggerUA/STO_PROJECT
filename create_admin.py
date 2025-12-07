from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password=generate_password_hash("admin123"), role="admin")
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin / admin123")
    else:
        print("Admin already exists.")
