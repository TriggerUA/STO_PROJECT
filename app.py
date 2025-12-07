from flask import Flask, render_template, request, redirect, session, url_for, flash
from models import db, User, Car, Order
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "replace-with-strong-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1987_QAZwsxEDC_1987@localhost/sto_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# --- Helpers ---
def current_user():
    if "username" in session:
        return User.query.filter_by(username=session["username"]).first()
    return None

def login_required():
    return "username" in session

# --- Routes ---
@app.route("/")
def home():
    return redirect(url_for("login"))

# ----------------- Login & Register -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if not user:
            # ask to register
            return render_template("login.html", ask_register=True, username=username)
        if not check_password_hash(user.password, password):
            msg = "Невірний пароль"
            return render_template("login.html", message=msg)
        # success
        session["username"] = user.username
        session["role"] = user.role
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"].strip()
    password = request.form["password"]
    role = request.form.get("role", "client")
    if User.query.filter_by(username=username).first():
        flash("Користувач вже існує.")
        return redirect(url_for("login"))
    hashed = generate_password_hash(password)
    user = User(username=username, password=hashed, role=role)
    db.session.add(user)
    db.session.commit()
    session["username"] = user.username
    session["role"] = user.role
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ----------------- Dashboard -----------------
@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))
    user = current_user()
    if user.role == "admin":
        return render_template("dashboard_admin.html", user=user)
    if user.role == "mechanic":
        return render_template("dashboard_mechanic.html", user=user)
    return render_template("dashboard_client.html", user=user)

# ----------------- Cars -----------------
@app.route("/cars")
def cars():
    if not login_required():
        return redirect(url_for("login"))
    user = current_user()
    if user.role == "admin":
        cars = Car.query.all()
    elif user.role == "client":
        cars = Car.query.filter_by(owner_id=user.id).all()
    else:
        cars = Car.query.all()
    return render_template("cars.html", cars=cars)

@app.route("/cars/add", methods=["GET", "POST"])
def car_add():
    if not login_required() or session.get("role") != "admin":
        return render_template("denied.html"), 403
    if request.method == "POST":
        model = request.form["model"].strip()
        plate = request.form["plate"].strip()
        owner_username = request.form["owner"].strip()
        owner = User.query.filter_by(username=owner_username).first()
        if not owner:
            return render_template("cars_add.html", message="Власник не знайдений")
        car = Car(model=model, plate=plate, owner_id=owner.id)
        db.session.add(car)
        db.session.commit()
        return redirect(url_for("cars"))
    users = User.query.all()
    return render_template("cars_add.html", users=users)

@app.route("/cars/delete/<int:car_id>")
def car_delete(car_id):
    if not login_required() or session.get("role") != "admin":
        return render_template("denied.html"), 403
    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
    return redirect(url_for("cars"))

# ----------------- Orders -----------------
@app.route("/orders")
def orders():
    if not login_required():
        return redirect(url_for("login"))
    user = current_user()
    if user.role == "admin":
        orders = Order.query.order_by(Order.id.desc()).all()
    elif user.role == "mechanic":
        orders = Order.query.filter_by(assigned_mechanic_id=user.id).all()
    else:  # client
        orders = Order.query.join(Car).filter(Car.owner_id == user.id).all()
    return render_template("orders.html", orders=orders)

@app.route("/orders/add", methods=["GET", "POST"])
def order_add():
    if not login_required() or session.get("role") != "admin":
        return render_template("denied.html"), 403
    mechanics_list = User.query.filter_by(role="mechanic").all()
    if request.method == "POST":
        car_id = int(request.form["car_id"])
        desc = request.form["service_description"].strip()
        price = request.form.get("price")
        assigned_id = request.form.get("assigned_mechanic_id")
        order = Order(
            car_id=car_id,
            service_description=desc,
            price=float(price) if price else None,
            status="new",
            assigned_mechanic_id=int(assigned_id) if assigned_id else None
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("orders"))
    cars = Car.query.all()
    return render_template("orders_add.html", cars=cars, mechanics=mechanics_list)

@app.route("/orders/<int:order_id>/update", methods=["GET", "POST"])
def order_update(order_id):
    if not login_required():
        return redirect(url_for("login"))
    order = Order.query.get(order_id)
    if not order:
        return redirect(url_for("orders"))
    user = current_user()
    if user.role not in ("admin", "mechanic"):
        return render_template("denied.html"), 403
    mechanics_list = User.query.filter_by(role="mechanic").all()
    if request.method == "POST":
        order.status = request.form.get("status", order.status)
        order.mechanic_notes = request.form.get("mechanic_notes", order.mechanic_notes)
        price = request.form.get("price")
        order.price = float(price) if price else order.price
        assigned_id = request.form.get("assigned_mechanic_id")
        order.assigned_mechanic_id = int(assigned_id) if assigned_id else None
        db.session.commit()
        return redirect(url_for("orders"))
    return render_template("orders_update.html", order=order, mechanics=mechanics_list)

@app.route("/orders/<int:order_id>/delete")
def order_delete(order_id):
    if not login_required() or session.get("role") != "admin":
        return render_template("denied.html"), 403
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for("orders"))

# ----------------- Mechanics -----------------
@app.route("/mechanics")
def mechanics():
    if not login_required() or session.get("role") != "admin":
        return render_template("denied.html"), 403
    mechanics = User.query.filter_by(role="mechanic").all()
    return render_template("mechanics.html", mechanics=mechanics)

@app.route("/mechanics/add", methods=["GET", "POST"])
def mechanics_add():
    if not login_required() or session.get("role") != "admin":
        return render_template("denied.html"), 403
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            return render_template("mechanics_add.html", message="Користувач уже існує")
        hashed = generate_password_hash(password)
        user = User(username=username, password=hashed, role="mechanic")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("mechanics"))
    return render_template("mechanics_add.html")

if __name__ == "__main__":
    app.run(debug=True)
