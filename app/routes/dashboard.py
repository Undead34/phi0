from flask import Blueprint, render_template, redirect, session, request, Response
from app.services.firebase import add_emails, get_all_emails, delete_email_by_id
import re

def is_valid_email(email):
    # Simple regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if 'user' in session:
        registered_users = get_all_emails()

        users_with_credentials = [user for user in registered_users if user.get('username') and user.get('password')]
        users_without_credentials = [user for user in registered_users if not (user.get('username') and user.get('password'))]

        stats = {'total_users': len(registered_users)}
        return render_template("dashboard.html", user=session['user'], users_with_credentials=users_with_credentials, users_without_credentials=users_without_credentials, stats=stats)
    else:
        return redirect("/login")

@dashboard_bp.post("/load_targets")
def load_targets():
    if request.method == 'POST':
        emails = request.form.get('emails', '')
        # Split emails by common separators and strip whitespace
        raw_email_list = re.split(r'[,\s;]+', emails)
        # Filter out invalid emails and duplicates
        email_list = []
        for email in raw_email_list:
            cleaned_email = email.strip().lower()
            if cleaned_email and is_valid_email(cleaned_email) and cleaned_email not in email_list:
                email_list.append(cleaned_email)
        
        add_emails(email_list)
        return redirect("/dashboard")
    
    return Response("Method Not Allowed, pelotudo!", status=405)

@dashboard_bp.post("/delete_email")
def delete_email():
    email_id = request.form.get('email_id')
    delete_email_by_id(email_id)
    return redirect("/dashboard")
