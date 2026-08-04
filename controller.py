from flask import current_app as app
from flask import render_template,request, redirect , url_for
from models import *

@app.route("/")
def homepage(): 
    return render_template("homepage.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("fname")
        email = request.form.get("email_id")
        password = request.form.get("password")
        c_password = request.form.get("c_password")
        role = request.form.get("role")
        user = db.session.query(User_Credentials).filter(User_Credentials.email == email.strip()).first()
        if user:
            return render_template("register.html", error_message="Email already exists")
        else:
            uc = User_Credentials(email=email, password=password, role=int(role))
            db.session.add(uc)
            db.session.commit() #save in db

        if password != c_password:
            return redirect(url_for("register"))
        print(name, email, password, c_password, role)
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    #check user credentials
    if request.method == "POST":
        uname = request.form.get("email_id")
        pwd = request.form.get("password")
        user = db.session.query(User_Credentials).filter(User_Credentials.email == uname.strip(), User_Credentials.password == pwd.strip()).first()
        if user:
            if user.role == 0:
                return render_template("Admin_templates/admin_dashboard.html")
            else:
                return redirect(url_for("register"))
        else:
            return redirect(url_for("register"))
            
    return render_template("login.html")



app_dct = [
    {"b_id": "123", "name": "John Doe", "Trek": "Everest Base Camp", "date": "2023-05-15", "status": "booked"},
    {"b_id": "456", "name": "Jane Smith", "Trek": "Annapurna Base Camp", "date": "2023-05-15", "status": "Pending"},
    {"b_id": "789", "name": "Bob Johnson", "Trek": "Kathmandu Valley", "date": "2023-05-16", "status": "cancelled"}
]

@app.route("/admin")
def admin_dashboard():
    return render_template("Admin_templates/admin_dashboard.html", bookings=app_dct, title = "dashboard")

@app.route("/add_trek")
def admin_add_new_trek():
    return render_template("Admin_templates/admin_add_new_trek.html")

@app.route("/manage_treks")
def admin_manage_treks():
    return render_template("Admin_templates/admin_manage_treks.html")