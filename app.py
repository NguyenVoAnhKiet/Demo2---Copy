from flask import Flask, render_template, redirect, url_for, session, g
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


# def login_required(func):
#     """Decorator to ensure the user is logged in before accessing a route."""
#     from functools import wraps

#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         if not session.get("logged_in"):
#             return redirect(url_for("auth.login"))
#         return func(*args, **kwargs)


#     return decorated_function
def login_required(f):
    """Decorator to ensure login is required."""

    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__  # Ensure function name is preserved for Flask
    return wrapper


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("auth.login"))


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


@app.before_request
def load_logged_in_user():
    """Load user information if logged in."""
    g.user = session.get("user")


if __name__ == "__main__":  # Khởi tạo cơ sở dữ liệu nếu cần
    app.run(debug=True)
