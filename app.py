from flask import Flask, render_template, request, redirect, url_for, session # type: ignore
import os
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session to work (set to something random in production)

# Dummy credentials
USERNAME = "admin"
PASSWORD = "radhe123"

@app.route("/")
def home():
    return "Welcome to login page! <a href='/login'>Login</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("move_file"))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/move_file", methods=["GET", "POST"])
def move_file():
    if "user" not in session:
        return redirect(url_for("login"))

    message = ""
    error = ""

    if request.method == "POST":
        source = request.form.get("source_path")
        destination = request.form.get("destination_path")

        print(f"Source: {source}, Destination: {destination}")  # Debugging output

        try:
            if not os.path.isfile(source):
                error = f"Source file does not exist: {source}"
            elif not os.path.isdir(destination):
                error = f"Destination is not a valid directory: {destination}"
            else:
                filename = os.path.basename(source)
                dest_path = os.path.join(destination, filename)
                shutil.move(source, dest_path)
                message = f"File moved to {dest_path}"
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("move_file.html", user=session["user"], message=message, error=error)


if __name__ == "__main__":
    app.run(debug=True)
