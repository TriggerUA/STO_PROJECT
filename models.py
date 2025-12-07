from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="client")  # admin, mechanic, client
    cars = db.relationship("Car", backref="owner", lazy=True)
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(120), nullable=False)
    plate = db.Column(db.String(30), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    orders = db.relationship("Order", backref="car", lazy=True)
    def __repr__(self):
        return f"<Car {self.plate} - {self.model}>"

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    service_description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="new")  # new, in_progress, done
    mechanic_notes = db.Column(db.String(500), nullable=True)
    def __repr__(self):
        return f"<Order {self.id} car={self.car_id} status={self.status}>"
