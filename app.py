from flask import Flask, render_template, redirect, url_for
from auth import auth
from auth.models import db
import os

app = Flask(__name__)
app.secret_key = "fakerfivecup"

# Cấu hình cơ sở dữ liệu
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'DemoDB')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Đăng ký Blueprint
app.register_blueprint(auth, url_prefix="/")


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("auth.login"))


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":  # Khởi tạo cơ sở dữ liệu nếu cần
    app.run(debug=True)
