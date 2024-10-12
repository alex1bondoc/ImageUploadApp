from flask import Flask, request, render_template, redirect, session
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__, static_folder="public")
app.secret_key = "hqop734ubqevwot7824bto"

app.config['UPLOAD_FOLDER'] = 'public/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

accounts = {
    "admin@gmail.com": "admin123",
    "test@gmail.com":"test123",
}
buttons = [
    ("Home", "/home"),
    ("Login", "/login"),
]

images = ["bmw6.png", "740iL.png", "rs5v8.png", "c63amg.png", "shelby.png", "lambo.png"]
size = 256, 256

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.context_processor
def inject_template_vars():
    return dict(buttons=buttons)

@app.route("/")
def index():
    return redirect("/home", code=302)

@app.route("/home")
def home():
    return render_template("index.html",
                           page="Home", images=images)

@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect("/home", code=302)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image = Image.open(file_path)
            image.thumbnail(size)
            image.save(file_path)
            images.append(filename)          
            return redirect("/upload", code=302)
    return render_template("upload.html", page="Upload")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    error = ""
    if "email" in request.form:
        email = request.form["email"]
        password = request.form["password"]
        if email in accounts and password==accounts[email]:
            session["email"] = email
            session["auth"] = True
            return redirect("/home", code=302)
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


