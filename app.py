import hashlib
import os
import secrets

import psycopg
from flask import Flask, render_template, request

app = Flask(__name__, template_folder=".")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")
    return psycopg.connect(database_url)


def initialize_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS registrations (
                    id BIGSERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    age INTEGER NOT NULL,
                    date_value DATE,
                    time_value TIME,
                    mobile VARCHAR(20) NOT NULL,
                    website TEXT,
                    gender VARCHAR(20) NOT NULL,
                    skills TEXT,
                    city VARCHAR(100) NOT NULL,
                    image_name TEXT NOT NULL,
                    image_mime VARCHAR(100) NOT NULL,
                    image_data BYTEA NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )


@app.get("/")
def form_page():
    return render_template("form.html")


@app.post("/register")
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    plain_password = request.form.get("password", "")
    age_value = request.form.get("age", "").strip()
    date_value = request.form.get("date") or None
    time_value = request.form.get("time") or None
    mobile = request.form.get("mobile", "").strip()
    website = request.form.get("website", "").strip() or None
    gender = request.form.get("gender", "").strip()
    skills = ",".join(request.form.getlist("skill"))
    city = request.form.get("city", "").strip()
    image = request.files.get("images")

    if not all((name, email, plain_password, age_value, mobile, gender, city)):
        return message_page("Please complete all required fields.", False), 400
    if len(plain_password) < 6:
        return message_page("Password must be at least 6 characters.", False), 400
    if not mobile.isdigit() or len(mobile) != 10:
        return message_page("Mobile number must contain exactly 10 digits.", False), 400

    try:
        age = int(age_value)
        if age <= 0:
            raise ValueError
    except ValueError:
        return message_page("Please enter a valid age.", False), 400

    if not image or not image.filename:
        return message_page("Please upload an image.", False), 400
    if not (image.mimetype or "").startswith("image/"):
        return message_page("Only image files are allowed.", False), 400

    image_data = image.read(5 * 1024 * 1024 + 1)
    if len(image_data) > 5 * 1024 * 1024:
        return message_page("Image must be less than 5 MB.", False), 400

    iterations = 600_000
    salt = secrets.token_bytes(16)
    password_digest = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode("utf-8"), salt, iterations
    ).hex()
    password_hash = (
        f"pbkdf2_sha256${iterations}${salt.hex()}${password_digest}"
    )

    try:
        initialize_database()
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO registrations
                    (name, email, password, age, date_value, time_value,
                     mobile, website, gender, skills, city,
                     image_name, image_mime, image_data)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        name, email, password_hash, age, date_value, time_value,
                        mobile, website, gender, skills, city,
                        image.filename, image.mimetype, image_data,
                    ),
                )
    except Exception:
        app.logger.exception("Registration could not be saved")
        return message_page("Database connection failed. Check DATABASE_URL.", False), 500

    return message_page("Data saved successfully.", True)


def message_page(message, success):
    color = "success" if success else "danger"
    title = "Success" if success else "Error"
    return f"""<!doctype html>
    <html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css' rel='stylesheet'>
    <title>{title}</title></head>
    <body class='bg-light'><main class='container py-5' style='max-width:700px'>
    <div class='alert alert-{color}'><h2>{title}</h2><p>{message}</p></div>
    <a class='btn btn-primary' href='/'>Go back</a></main></body></html>"""


@app.errorhandler(413)
def image_too_large(_error):
    return message_page("Image must be less than 5 MB.", False), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=True)