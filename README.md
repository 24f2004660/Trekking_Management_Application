# Trekking Management Application

A full-stack web application for managing treks, staff, and trekkers, built as
a project for **Modern Application Development I**. The system supports three
roles — **Admin**, **Staff**, and **User (Trekker)** — each with their own
dashboard and permissions, following an MVC-style architecture.

## Features

**Admin**
- Dashboard with counts of treks, users, staff, and bookings
- Add, edit, and delete treks; assign staff to treks
- Approve/reject staff registrations, blacklist/reinstate users
- View and cancel bookings

**Staff**
- Dashboard showing assigned treks and participant counts
- Manage individual treks: view participants, update available slots and
  trek status, mark treks as completed
- Search/filter participants across all assigned treks

**User (Trekker)**
- Browse open treks with search, difficulty, and location filters
- Book available treks and view booking history
- View completed treks

**Common**
- Registration and login with role-based redirection
- Editable profile pages for both users and staff

## Tech Stack

| Layer    | Technology |
|----------|------------|
| Backend  | Python, Flask |
| Database | SQLite, Flask-SQLAlchemy |
| Frontend | HTML, Jinja2 templates, Bootstrap 5, Bootstrap Icons |

## Project Structure

```
├── app.py                     # Flask app setup and DB configuration
├── controller.py              # Routes / view logic (all endpoints)
├── models.py                  # SQLAlchemy models
├── instance/trekking.sqlite3  # SQLite database
├── static/
│   ├── main.css
│   └── schema.png             # Database schema diagram
└── templates/
    ├── base.html, homepage.html, login.html, register.html, profile.html
    ├── Admin_templates/
    ├── Staff_templates/
    └── User_templates/
```

## Database Schema

The application uses five related tables: `User_Credentials`, `user_profile`,
`staff_profile`, `Trek`, and `Booking`. See `static/schema.png` for the full
entity-relationship diagram.

- A `User_Credentials` record holds login info and a `role` (admin / staff /
  user) and links to exactly one `user_profile` or `staff_profile`.
- A `Trek` is created by an Admin and assigned to a `staff_profile`.
- A `Booking` links a `user_profile` to a `Trek`, with a status of
  `Booked` / `Cancelled` / `Completed`.

## Setup & Running Locally

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Trekking_Management
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

3. **Run the application**
   ```bash
   python app.py
   ```
   The database (`trekking.sqlite3`) is included; the app connects to it
   automatically on startup.

4. **Open in browser**
   ```
   http://127.0.0.1:5000/
   ```

## Notes

- Roles are stored as strings/integers: `0` = Admin, `1` = Staff, `2` = User.
- This project was built as a learning exercise for Modern App Dev I, with an
  emphasis on the MVC pattern (Model → `models.py`, View → `templates/`,
  Controller → `controller.py`).

## Author

Ashutosh Ray Mohapatra
