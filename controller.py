print(app)
from app import *

@app.route("/login/")
def login():
    return render_template("login.html")