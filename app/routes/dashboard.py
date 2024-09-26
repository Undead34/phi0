from flask import Blueprint, render_template, redirect, session, request, Response
from app.services.firebase import add_emails, get_all_emails, delete_email_by_id
import re

def is_valid_email(email):
    """Simple regex for email validation."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def clean_and_validate_emails(raw_emails):
    """Clean and validate a list of emails."""
    raw_email_list = re.split(r'[,\s;]+', raw_emails)
    email_set = set()
    invalid_emails = []
    
    for email in raw_email_list:
        cleaned_email = email.strip().lower()
        if cleaned_email:
            if is_valid_email(cleaned_email):
                email_set.add(cleaned_email)
            else:
                invalid_emails.append((cleaned_email, "Invalid email format"))
        else:
            invalid_emails.append((cleaned_email, "Empty email"))

    valid_emails = list(email_set)
    return valid_emails, invalid_emails

def categorize_users(users: list[dict]):
    """Categorize users into those with and without credentials."""
    users_with_credentials = [user for user in users if user.get('username') and user.get('password')]
    users_without_credentials = [user for user in users if not (user.get('username') and user.get('password'))]
    return users_with_credentials, users_without_credentials

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if 'user' in session:
        registered_users = get_all_emails()
        users_with_credentials, users_without_credentials = categorize_users(registered_users)
        users_visited = [user for user in registered_users if (user.get('visited') or user.get('password'))]
        stats = {'total_users': len(registered_users), "users_visited": len(users_visited)}

        return render_template("dashboard.html", user=session['user'], users_with_credentials=users_with_credentials, users_without_credentials=users_without_credentials, stats=stats, users_visited=users_visited)
    else:
        return redirect("/login")

@dashboard_bp.post("/load_targets")
def load_targets():
    if request.method == 'POST':
        emails = request.form.get('emails', '')
        email_list, _ = clean_and_validate_emails(emails)
        
        add_emails(email_list)

        return redirect("/dashboard")
    
    return Response("Method Not Allowed", status=405)

@dashboard_bp.post("/delete_email")
def delete_email():
    email_id = request.form.get('email_id')
    delete_email_by_id(email_id)
    return redirect("/dashboard")
