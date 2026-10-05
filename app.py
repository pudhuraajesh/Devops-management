from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "responses.db"


# ==========================================
# DATABASE
# ==========================================

def init_db():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# PIPELINE
# ==========================================

@app.route("/pipeline")
def pipeline():

    return render_template("pipeline.html")


# ==========================================
# MICROSERVICES
# ==========================================

@app.route("/services")
def services():

    return render_template("services.html")


# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():

    return """
    <h1>DevOps Deployment Center</h1>

    <p>
        A Flask-based application demonstrating
        DevOps practices including Git, GitHub,
        CI/CD, automated testing, cloud deployment
        and microservices architecture.
    </p>

    <a href="/">Back to Home</a>
    """


# ==========================================
# SUBMIT RESPONSE
# ==========================================

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:

        return "All fields are required.", 400

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO responses
        (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))

    connection.commit()
    connection.close()

    return redirect(url_for("success"))


# ==========================================
# SUCCESS
# ==========================================

@app.route("/success")
def success():

    return render_template("success.html")


# ==========================================
# RESPONSES
# ==========================================

@app.route("/responses")
def responses():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, message
        FROM responses
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return render_template(
        "responses.html",
        responses=data
    )


# ==========================================
# DELETE RESPONSE
# ==========================================

@app.route("/delete/<int:response_id>", methods=["POST"])
def delete_response(response_id):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM responses WHERE id = ?",
        (response_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("responses"))


# ==========================================
# DELETE ALL
# ==========================================

@app.route("/delete-all", methods=["POST"])
def delete_all():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM responses")

    connection.commit()
    connection.close()

    return redirect(url_for("responses"))


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "application": "DevOps Deployment Center"
    }


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)