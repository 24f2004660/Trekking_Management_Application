from flask import current_app as app
from flask import render_template,request, redirect , url_for
from models import *
from datetime import datetime

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
        ph_no = request.form.get("phone")
        address = request.form.get("address")
        user = db.session.query(User_Credentials).filter(User_Credentials.email == email.strip()).first()
        if user:
            return render_template("register.html", error_message="Email already exists")
        if password != c_password:
                return render_template("register.html", error_pass="Passwords do not match")
        
        uc = User_Credentials(email=email, password=password, role=role)
        db.session.add(uc)
        db.session.commit()
        if role == '2':
            u_profile = user_profile(user_id=uc.id,name=name, address=address, phone_number=ph_no)
            db.session.add(u_profile)
        else:
            experience = request.form.get("exp")
            s_profile = staff_profile(staff_id=uc.id,name=name, address=address, phone_number=ph_no, experience=experience)
            db.session.add(s_profile)
        db.session.commit()
            
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
            
            if user.role == '0':
                return redirect(url_for("admin_dashboard"))
            elif user.role == '1':
                return redirect(url_for("staff_dashboard"))
            elif user.role == '2':
                return redirect(url_for("user_dashboard"))
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

#Admin
@app.route("/admin")
def admin_dashboard():
    return render_template("Admin_templates/admin_dashboard.html")

from datetime import datetime

@app.route("/add_trek", methods=["GET", "POST"])
def admin_add_new_trek():
    if request.method == "POST":
        t_name = request.form.get("trek_name")
        location = request.form.get("location")
        diff = request.form.get("difficulty")
        duration = request.form.get("duration")
        avl_slots = request.form.get("available_slots")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        assigned_staff = request.form.get("assigned_staff")
        status = request.form.get("status")
        description = request.form.get("description")

        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        # print("DEBUG:", t_name, location, diff, duration, avl_slots, start_date, end_date, assigned_staff, status)
        new_trek = Trek(
            t_name=t_name, location=location, diff=diff,
            duration=int(duration), avl_slots=int(avl_slots),
            start_date=start_date, end_date=end_date,
            assign_s_id=int(assigned_staff), status=status,
            description=description
        )
        db.session.add(new_trek)
        db.session.commit()
    return render_template("Admin_templates/admin_add_new_trek.html")

@app.route("/manage_treks")
def admin_manage_treks():
    treks = db.session.query(Trek).filter().all()
    return render_template("Admin_templates/admin_manage_treks.html", treks=treks)

@app.route("/manage_staffs")
def admin_manage_staffs():
    s_data = get_staff_data()
    return render_template("Admin_templates/admin_manage_staffs.html", s_data=s_data)
    
@app.route("/manage_users")
def admin_manage_users():
    u_data = get_user_data()
    return render_template("Admin_templates/admin_manage_users.html", u_data=u_data)

#User
@app.route("/user")
def user_dashboard():
    return render_template("User_templates/user_dashboard.html")


#satff
@app.route("/staff")
def staff_dashboard():
    return render_template("Staff_templates/staff_dashboard.html")



#Additional python functions
def get_user_data():
    u_data = db.session.query(user_profile).filter().all()
    return u_data

def get_staff_data():
    s_data = db.session.query(staff_profile).filter().all()
    return s_data

def search_staff(id):
    staff_searched = db.session.query(staff_profile).filter(staff_profile.staff_id == id).first()
    return staff_searched

def search_user(id):
    user_searched = db.session.query(user_profile).filter(user_profile.user_id == id).first()
    return user_searched