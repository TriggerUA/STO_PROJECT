from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password=generate_password_hash("admin123"), role="admin")
        db.session.add(admin)
        print("Admin created: admin / admin123")
    else:
        print("Admin already exists.")
    mechanics = [
        {"username": "Yura", "password": "Sikorsky2005"},
        {"username": "Yarik", "password": "Pivo2005"},
    ]

    for mech in mechanics:
        if not User.query.filter_by(username=mech["username"]).first():
            m = User(username=mech["username"], password=generate_password_hash(mech["password"]), role="mechanic")
            db.session.add(m)
            print(f"Mechanic created: {mech['username']} / {mech['password']}")
        else:
            print(f"Mechanic {mech['username']} already exists.")

    db.session.commit()
