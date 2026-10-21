
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    roll_number = request.form.get("roll_number", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    college = request.form.get("college", "").strip()
    team_name = request.form.get("team_name", "").strip()
    course = request.form.get("course", "").strip()

    # Basic server-side validation
    if not name or not email or not phone or not course:
        return "Please complete all required fields.", 400

    if not phone.isdigit() or len(phone) != 10:
        return "Please enter a valid 10-digit phone number.", 400
    
    if not name or not roll_number or not email or not phone or not course:
         return "Please complete all required fields.", 400

    return render_template(
        "success.html",
        name=name,
        roll_number=roll_number,
        email=email,
        phone=phone,
        college=college,
        team_name=team_name,
        course=course
    )


if __name__ == "__main__":
    app.run(debug=True)
