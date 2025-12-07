from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="client")  # admin, mechanic, client
    cars = db.relationship("Car", backref="owner", lazy=True)
    orders_assigned = db.relationship("Order", backref="assigned_mechanic", lazy=True, foreign_keys='Order.assigned_mechanic_id')

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(120), nullable=False)
    plate = db.Column(db.String(30), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    orders = db.relationship("Order", backref="car", lazy=True)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    service_description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="new")  # new, in_progress, done
    mechanic_notes = db.Column(db.String(500), nullable=True)
    assigned_mechanic_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    services = db.relationship("Service", secondary="order_services", backref="orders")
    invoice = db.relationship("Invoice", backref="order", uselist=False)
    parts = db.relationship("Part", secondary="order_parts", backref="orders")

class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

class Invoice(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid_at = db.Column(db.DateTime, server_default=db.func.now())

class Part(db.Model):
    __tablename__ = "parts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

order_services = db.Table('order_services',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)

order_parts = db.Table('order_parts',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('part_id', db.Integer, db.ForeignKey('parts.id'), primary_key=True)
)
