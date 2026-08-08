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
                staff_p = search_staff(user.id)
                if staff_p.status == 1:
                    return redirect(url_for("staff_dashboard", staff_id = user.id))
                elif staff_p.status == 0:
                    status = "Pending"
                    return render_template("s_status.html", status = status)
                else:
                    status = ""
                    return render_template("s_status.html", status= status)

            elif user.role == '2':
                user_p = search_user(user.id)
                if user_p.status == 0:
                    return redirect(url_for("user_dashboard", user_id = user.id))
                else:
                    return render_template("u_status.html")
            else:
                return redirect(url_for("register"))
        else:
            return redirect(url_for("register"))
            
    return render_template("login.html")

@app.route("/profile")
def profile():
    user_id = request.args.get("user_id")
    staff_id = request.args.get("staff_id")
    edit = request.args.get("edit")

    if staff_id:
        role = "staff"
        s_profile = search_staff(staff_id)
        name = s_profile.name
        address = s_profile.address
        phone = s_profile.phone_number
        email = s_profile.staff_back.email
        experience = s_profile.experience
        return render_template("profile.html", role=role, staff_id=staff_id,
                                name=name, address=address, phone=phone,
                                email=email, experience=experience, edit=edit)
    else:
        role = "user"
        u_profile = search_user(user_id)
        name = u_profile.name
        address = u_profile.address
        phone = u_profile.phone_number
        email = u_profile.user_back.email
        return render_template("profile.html", role=role, user_id=user_id,
                                name=name, address=address, phone=phone,
                                email=email, edit=edit)


@app.route("/update_profile", methods=["POST"])
def update_profile():
    role = request.form.get("role")
    name = request.form.get("name")
    phone = request.form.get("phone")
    address = request.form.get("address")

    if role == "staff":
        staff_id = request.form.get("staff_id")
        experience = request.form.get("experience")

        profile = search_staff(staff_id)
        profile.name = name
        profile.phone_number = phone
        profile.address = address
        profile.experience = experience
        db.session.commit()

        return redirect(url_for("profile", staff_id=staff_id))

    else:
        user_id = request.form.get("user_id")

        profile = search_user(user_id)
        profile.name = name
        profile.phone_number = phone
        profile.address = address
        db.session.commit()

        return redirect(url_for("profile", user_id=user_id))

#Admin
@app.route("/admin")
def admin_dashboard():
    t_count = db.session.query(Trek).count()
    u_count = db.session.query(user_profile).count()
    s_count = db.session.query(staff_profile).count()
    b_count = db.session.query(Booking).count()
    booking = db.session.query(Booking).filter().all()
    return render_template("Admin_templates/admin_dashboard.html" , t_count = t_count, u_count = u_count ,s_count = s_count , b_count = b_count , bookings = booking)

@app.route("/add_trek", methods=["GET", "POST"])
def admin_add_new_trek():
    staffs = get_staff_data()
    if request.method == "POST":
        t_name = request.form.get("trek_name")
        location = request.form.get("location")
        diff = request.form.get("difficulty")
        duration = request.form.get("duration")
        total_slots = request.form.get("total_slots")
        avl_slots = request.form.get("total_slots")
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
            duration=int(duration),total_slots = int(total_slots) , avl_slots=int(avl_slots),
            start_date=start_date, end_date=end_date,
            assign_s_id=int(assigned_staff), status=status,
            description=description
        )
        db.session.add(new_trek)
        db.session.commit()
    return render_template("Admin_templates/admin_add_new_trek.html", staffs=staffs)

@app.route("/manage_treks")
def admin_manage_treks():
    search = request.args.get("search")

    if search:
        treks = db.session.query(Trek).filter(Trek.t_name.like("%" + search + "%")).all()
    else:
        treks = db.session.query(Trek).filter().all()

    return render_template("Admin_templates/admin_manage_treks.html", treks=treks, search=search)

@app.route("/manage_staffs")
def admin_manage_staffs():
    search = request.args.get("search")
    status = request.args.get("status")

    query = db.session.query(staff_profile)

    if search:
        query = query.filter(staff_profile.name.like("%" + search + "%"))

    if status and status != "all":
        query = query.filter(staff_profile.status == int(status))

    s_data = query.all()

    return render_template("Admin_templates/admin_manage_staffs.html",
                            s_data=s_data, search=search, status=status)
    
@app.route("/manage_users")
def admin_manage_users():
    search = request.args.get("search")
    status = request.args.get("status")

    query = db.session.query(user_profile)

    if search:
        query = query.filter(user_profile.name.like("%" + search + "%"))

    if status and status != "all":
        query = query.filter(user_profile.status == int(status))

    u_data = query.all()

    return render_template("Admin_templates/admin_manage_users.html",
                            u_data=u_data, search=search, status=status)

@app.route("/reject", methods=["GET","POST"])
def reject_user():
    user_id = request.args.get("user_id")
    user = search_user(user_id)
    user.status = "1"# blacklisted
    db.session.commit()
    return redirect(url_for("admin_manage_users"))

@app.route("/approve_user", methods = ["GET","POST"])
def approve_user():
    user_id = int(request.args.get("user_id"))
    user_searched = search_user(user_id)
    user_searched.status = "0"
    db.session.commit()
    return redirect(url_for("admin_manage_users"))

@app.route("/edit_trek")
def admin_edit_trek():
    trek_id = request.args["trek_id"]
    trek_searched = search_trek(trek_id)
    staffs = get_staff_data()
    return render_template("Admin_templates/admin_edit_trek.html", trek_data = trek_searched , staffs = staffs)

@app.route("/update_trek", methods=["GET", "POST"])
def update_trek():
    t_id = request.form.get("t_id")
    t_name = request.form.get("trek_name")
    start_date = request.form.get("start_date")
    location = request.form.get("location")
    difficulty = request.form.get("difficulty")
    duration = request.form.get("duration")
    total_slots = request.form.get("total_slots")
    avl_slots = request.form.get("avl_slots")
    end_date = request.form.get("end_date")
    asn_staff = request.form.get("asn_staff")
    status = request.form.get("status")
    description = request.form.get("description")

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    old_trek_details = db.session.query(Trek).filter(Trek.trek_id == t_id).first()

    old_trek_details.t_name = t_name
    old_trek_details.start_date = start_date
    old_trek_details.end_date = end_date
    old_trek_details.location = location
    old_trek_details.diff = difficulty
    old_trek_details.duration = duration
    old_trek_details.total_slots = total_slots
    old_trek_details.avl_slots = avl_slots
    old_trek_details.assign_s_id = asn_staff
    old_trek_details.status = status
    old_trek_details.description = description

    db.session.commit() #saved

    return redirect(url_for("admin_manage_treks"))

@app.route("/blacklist_staff")
def reject_staff():
    staff_id = request.args.get("staff_id")
    staff_searched = search_staff(staff_id)
    staff_searched.status = 2
    db.session.commit()
    return redirect(url_for("admin_manage_staffs"))

@app.route("/approve_staff")
def approve_staff():
    staff_id = request.args.get("staff_id")
    staff_searched = search_staff(staff_id)
    staff_searched.status = 1
    db.session.commit()
    return redirect(url_for("admin_manage_staffs"))

@app.route("/cancel_booking")
def cancel_booking():
    booking_id = request.args.get("booking_id")
    booking_searched = search_booking(booking_id)
    booking_searched.status = "Cancelled"
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/delete_trek")
def delete_trek():
    trek_id = request.args.get("trek_id")

    trek = search_trek(trek_id)

    if trek:
        db.session.delete(trek)
        db.session.commit()

    return redirect(url_for("admin_manage_treks"))

#User
@app.route("/user")
def user_dashboard():
    user_id = request.args.get("user_id")
    search = request.args.get("search")
    difficulty = request.args.get("difficulty")
    location = request.args.get("location")

    query = db.session.query(Trek).filter(Trek.status == "1")

    if search:
        query = query.filter(Trek.t_name.like("%" + search + "%"))

    if difficulty and difficulty != "All":
        query = query.filter(Trek.diff == difficulty)

    if location and location != "All":
        query = query.filter(Trek.location == location)

    trek = query.all()

    all_locations = db.session.query(Trek.location).distinct().all()
    locations = [l[0] for l in all_locations]

    booked_trek_ids = get_user_booked_trek_ids(user_id) if user_id else []
    my_bookings = get_user_bookings(user_id) if user_id else []

    user_p = search_user(user_id)
    user_name = (user_p.name).split()

    return render_template(
        "User_templates/user_dashboard.html",
        trek=trek,
        user_id=user_id,
        booked_trek_ids=booked_trek_ids,
        my_bookings=my_bookings,
        user_name=user_name[0],
        locations=locations,
        search=search,
        difficulty=difficulty,
        location=location
    )


@app.route("/user_book")
def user_booking():
    trek_id = request.args.get("trek_id")
    user_id = request.args.get("user_id")

    trek = search_trek(trek_id)

    if trek and trek.avl_slots > 0 and trek.status == "1":
        b_data = Booking(user_id=int(user_id), trek_id=int(trek_id), booking_date=datetime.now(), status="Booked")
        db.session.add(b_data)

        trek.avl_slots -= 1
        if trek.avl_slots == 0:
            trek.status = "0"  # optional: auto-close when slots hit 0, see note below

        db.session.commit()

    return redirect(url_for("user_dashboard", user_id=user_id))

@app.route("/user_history")
def user_history():
    user_id = request.args.get("user_id")
    history = get_user_completed_treks(user_id) if user_id else []
    return render_template(
        "User_templates/user_history.html",
        history=history,
        user_id=user_id
    )

#satff
@app.route("/staff")
def staff_dashboard():
    staff_id = request.args.get("staff_id")

    get_staff =search_staff(staff_id)
    staff_name = (get_staff.name).split()

    assigned_treks = db.session.query(Trek).filter(Trek.assign_s_id == staff_id).all()
    assigned_trek = db.session.query(Trek).filter(Trek.assign_s_id == staff_id).count()
    open_trek = db.session.query(Trek).filter(Trek.assign_s_id == staff_id, Trek.status == "1").count()
    participants = db.session.query(Booking).join(Trek).filter(Trek.assign_s_id == staff_id, Booking.status == "Booked").count()

    trek_participant_counts = {}
    for trek in assigned_treks:
        count = 0
        for booking in trek.bookings:
            if booking.status == "Booked":
                count += 1
        trek_participant_counts[trek.trek_id] = count

    return render_template(
        "Staff_templates/staff_dashboard.html",
        a_trek_count=assigned_trek,
        open_trek=open_trek,
        participants=participants,
        assigned_treks=assigned_treks,
        staff_id=staff_id,
        trek_participant_counts=trek_participant_counts,
        staff_name = staff_name[0]
    )

@app.route("/s_manage_trek")
def manage_trek():
    staff_id = request.args.get("staff_id")
    trek_id = request.args.get("trek_id")
    search = request.args.get("search")

    trek = search_trek(trek_id)

    participants = []
    for booking in trek.bookings:
        if booking.status == "Booked":
            user = search_user(booking.user_id)
            participants.append({"name": user.name,"email": user.user_back.email,"booking_date": booking.booking_date,"status": booking.status})

    if search:
        participants = [p for p in participants if search.lower() in p["name"].lower()]

    return render_template("Staff_templates/staff_manage_trek.html",trek=trek,participants=participants ,staff_id = staff_id, search=search)

@app.route("/staff_treks")
def staff_my_treks():
    staff_id = request.args.get("staff_id")
    search = request.args.get("search")

    query = db.session.query(Trek).filter(Trek.assign_s_id == staff_id)

    if search:
        query = query.filter(Trek.t_name.like("%" + search + "%"))

    assigned_treks = query.all()

    return render_template(
        "Staff_templates/staff_my_treks.html",
        assigned_treks=assigned_treks,
        staff_id=staff_id,
        search=search
    )

@app.route("/reset_trek_slots")
def reset_trek_slots():
    trek_id = request.args.get("trek_id")
    staff_id = request.args.get("staff_id")

    trek = search_trek(trek_id)
    if trek:
        trek.avl_slots = trek.total_slots
        db.session.commit()

    return redirect(url_for("manage_trek", trek_id=trek_id, staff_id=staff_id))

@app.route("/staff_participants")
def staff_participants():
    staff_id = request.args.get("staff_id")
    search = request.args.get("search")
    status = request.args.get("status")

    all_bookings = (
        db.session.query(Booking)
        .join(Trek)
        .filter(Trek.assign_s_id == staff_id)
        .all()
    )

    participants = []
    for booking in all_bookings:
        user = search_user(booking.user_id)
        trek = search_trek(booking.trek_id)
        participants.append({
            "name": user.name,
            "email": user.user_back.email,
            "trek_name": trek.t_name,
            "booking_date": booking.booking_date,
            "status": booking.status
        })

    if search:
        search_lower = search.lower()
        participants = [
            p for p in participants
            if search_lower in p["name"].lower() or search_lower in p["trek_name"].lower()
        ]

    if status and status != "all":
        participants = [p for p in participants if p["status"] == status]

    return render_template(
        "Staff_templates/staff_participants.html",
        participants=participants,
        staff_id=staff_id,
        search=search,
        status=status
    )

@app.route("/update_trek_slots", methods=["POST"])
def update_trek_slots():
    trek_id = request.form.get("trek_id")
    staff_id = request.form.get("staff_id")
    avl_slots = request.form.get("avl_slots")
    status = request.form.get("status")

    trek = search_trek(trek_id)
    if trek:
        trek.avl_slots = int(avl_slots)
        trek.status = status
        db.session.commit()

    return redirect(url_for("staff_dashboard", staff_id=staff_id))

@app.route("/mark_trek_completed")
def mark_trek_completed():
    trek_id = request.args.get("trek_id")
    staff_id = request.args.get("staff_id")

    trek = search_trek(trek_id)
    if trek:
        for booking in trek.bookings:
            if booking.status == "Booked":
                booking.status = "Completed"
        db.session.commit()

    return redirect(url_for("manage_trek", trek_id=trek_id, staff_id=staff_id))



#Additional python functions
def get_user_data():
    u_data = db.session.query(user_profile).filter().all()
    return u_data

def get_staff_data():
    s_data = db.session.query(staff_profile).filter().all()
    return s_data

def get_trek_data():
    t_data = db.session.query(Trek).filter().all()
    return t_data

def get_book_data():
    b_data = db.session.query(Booking).filter().all()
    return b_data

def search_staff(id):
    staff_searched = db.session.query(staff_profile).filter(staff_profile.staff_id == id).first()
    return staff_searched

def search_user(id):
    user_searched = db.session.query(user_profile).filter(user_profile.user_id == id).first()
    return user_searched

def search_trek(id):
    trek_searched = db.session.query(Trek).filter(Trek.trek_id == id).first()
    return trek_searched

def search_booking(id):
    booking_searched = db.session.query(Booking).filter(Booking.booking_id == id).first()
    return booking_searched

def get_user_booked_trek_ids(user_id):
    bookings = db.session.query(Booking).filter(Booking.user_id == user_id,Booking.status == "Booked").all()
    return [b.trek_id for b in bookings]

def get_user_bookings(user_id):
    bookings = db.session.query(Booking).filter(Booking.user_id == user_id).all()
    result = []
    for b in bookings:
        trek = search_trek(b.trek_id)
        result.append({
            "trek_name": trek.t_name ,
            "booking_date": b.booking_date,
            "status": b.status
        })
    return result

def get_user_completed_treks(user_id):
    bookings = (
        db.session.query(Booking)
        .filter(Booking.user_id == user_id, Booking.status == "Completed")
        .all()
    )
    result = []
    for b in bookings:
        trek = search_trek(b.trek_id)
        result.append({
            "trek_name": trek.t_name,
            "location": trek.location,
            "start_date": trek.start_date,
            "end_date": trek.end_date,
            "booking_date": b.booking_date,
        })
    return result
