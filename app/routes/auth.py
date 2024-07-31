from flask import Blueprint, render_template, redirect, request, session, Response
from argon2.exceptions import VerifyMismatchError
from app.services.firebase import create_user, get_user_by_email
from app.services.password import ph

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        account = request.form.get("account", "").strip()
        password = request.form.get("password", "").strip()
        display_name = request.form.get("display_name", "")

        if not account:
            return Response(render_template("register.html", error_message="Email is empty"), status=400)
        if not password:
            return Response(render_template("register.html", error_message="Password is empty"), status=400)

        try:
            create_user(account, password, display_name)
            return redirect("/login")
        except ValueError as e:
            return Response(render_template("register.html", error_message=str(e)), status=400)
        except Exception as e:
            return Response(render_template("register.html", error_message="Unexpected error occurred"), status=400)

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect("/dashboard")
    
    if request.method == "POST":
        account = request.form.get("account", "").strip()
        password = request.form.get("password", "").strip()

        if not account:
            return Response(render_template("login.html", error_message="Email is empty"), status=400)
        if not password:
            return Response(render_template("login.html", error_message="Password is empty"), status=400)
        
        try:
            user_data = get_user_by_email(account)

            if not user_data or not user_data.get("password_hash"):
                raise ValueError("Invalid email or password")

            stored_password_hash = user_data["password_hash"]

            ph.verify(stored_password_hash, password)

            session['user'] = {
                'uid': user_data["uid"],
                'email': user_data["email"],
                'display_name': user_data["display_name"]
            }

            return redirect("/dashboard")

        except (ValueError, VerifyMismatchError):
            return Response(render_template("login.html", error_message="Invalid email or password"), status=400)
        except Exception as e:
            print(e)
            return Response(render_template("login.html", error_message="An unexpected error occurred"), status=500)

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/login")
