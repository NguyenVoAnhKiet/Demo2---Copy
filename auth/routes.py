from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import db, User
import re
import hashlib

# from flask_login import login_user
auth = Blueprint("auth", __name__)


# Hàm kiểm tra định dạng email
def is_valid_email(email):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email)


# Hàm kiểm tra định dạng mật khẩu
def is_valid_password(password):
    if (
        len(password) >= 8
        and len(password) <= 40
        and re.search(r"[A-Z]", password)
        and re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ):
        return True
    return False


# Hàm băm mật khẩu bằng SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.password == hash_password(password):
            flash("Login successful!", "success")
            session["user_id"] = user.user_id
            session["username"] = user.username
            return redirect(url_for("home"))
        else:
            flash(
                "Invalid username or password.", "danger"
            )  # Kiểm tra xem phiên đã hết hạn chưa
    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phonenumber = request.form["phonenumber"]
        gender = request.form["gender"].capitalize()

        if not is_valid_email(email):
            flash("Invalid email format.", "danger")
        elif not is_valid_password(password):
            flash(
                "Password must be 8-40 characters long, include at least one uppercase letter and one special character.",
                "danger",
            )
        elif User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
        # Kiểm tra số điện thoại: chỉ nhận số và đúng 10 ký tự
        elif not phonenumber.isdigit() or len(phonenumber) != 10:
            flash(
                "Phone number must be 10 digits long and contain only numbers.",
                "danger",
            )
        else:
            # Băm mật khẩu trước khi lưu
            hashed_password = hash_password(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                phonenumber=phonenumber,
                gender=gender,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful!", "success")
            return redirect(url_for("auth.login"))
    return render_template("signup.html")


@auth.route("/logout")
def logout():
    # Xóa toàn bộ dữ liệu trong session
    session.clear()  # Xóa tên người dùng khỏi session

    # Xóa cookie nếu có
    resp = redirect(url_for("auth.login"))
    resp.set_cookie("username", "", expires=0)
    resp.set_cookie("password", "", expires=0)
    # Xóa tất cả thông báo flash để tránh hiển thị lại
    flash("You have been logged out.", "info")
    return resp  # Trả về response đã xóa cookie và redirect
