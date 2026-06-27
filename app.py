from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from models import db, User, Letter, Notification

app = Flask(__name__)

app.config["SECRET_KEY"] = "CHANGE_THIS_SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route("/")
@login_required
def home():

    recent_letters = (
        Letter.query.filter_by(
            receiver_id=current_user.id,
            deleted_by_receiver=False
        )
        .order_by(Letter.created_at.desc())
        .limit(5)
        .all()
    )

    unread_count = Letter.query.filter_by(
        receiver_id=current_user.id,
        is_read=False,
        deleted_by_receiver=False
    ).count()

    sent_count = Letter.query.filter_by(
        sender_id=current_user.id,
        deleted_by_sender=False
    ).count()

    received_count = Letter.query.filter_by(
        receiver_id=current_user.id,
        deleted_by_receiver=False
    ).count()

    return render_template(
        "home.html",
        recent_letters=recent_letters,
        unread_count=unread_count,
        sent_count=sent_count,
        received_count=received_count
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        exists = User.query.filter_by(
            username=username
        ).first()

        if exists:
            flash("이미 존재하는 아이디입니다.")
            return redirect(url_for("register"))

        user = User(
            username=username,
            password=generate_password_hash(password),
            created_at=datetime.utcnow()
        )

        db.session.add(user)
        db.session.commit()

        flash("회원가입이 완료되었습니다.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            user.last_login = datetime.utcnow()

            db.session.commit()

            login_user(user)

            return redirect(url_for("home"))

        flash("아이디 또는 비밀번호가 올바르지 않습니다.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/health")
def health():
    return {
        "status": "ok"
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
