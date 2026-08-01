from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/login/")
def login():
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

if __name__ == '__main__':
    app.run(debug=True)
