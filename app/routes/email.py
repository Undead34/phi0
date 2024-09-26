from flask import Blueprint, current_app, request, redirect, Response, render_template
from threading import Thread

from app.services.email import start_send_emails_async
from app.services.firebase import get_all_emails, update_email_status, get_user_by_id

email_bp = Blueprint('email', __name__)

@email_bp.get('/email-template')
def email():
    return render_template("emails/microsoft.html")

@email_bp.get('/email-template-hatsune-miku-mirai')
def email_test():
    app = current_app._get_current_object()
    base_url = request.url_root.rstrip('/')
    thread = Thread(target=start_send_emails_async, args=(app, [("gmaizo@netreadysolutions.com", "no-update"), ("maizogabriel@gmail.com", "no-update")], base_url, "emails/microsoft.html"))
    thread.start()

    return render_template("emails/microsoft.html")

@email_bp.route('/send-emails')
def send_emails():
    registered_users = get_all_emails()
    emails = []

    for user in registered_users:
        if user['email'] == 'anonymous@example.com':
            update_email_status(user['id'], 'unknown')
        else:
            emails.append((user['email'], user['id']))

    app = current_app._get_current_object()
    base_url = request.url_root.rstrip('/')
    thread = Thread(target=start_send_emails_async, args=(app, emails, base_url, "emails/microsoft.html"))
    thread.start()

    return redirect("/dashboard")


@email_bp.route('/send-email/<email_id>', methods=['POST'])
def send_email(email_id):
    user = get_user_by_id(email_id)
    if user:
        if user['email'] == 'anonymous@example.com':
            update_email_status(email_id, 'unknown')
            return Response("Cannot send email to anonymous@example.com", status=403)

        app = current_app._get_current_object()
        base_url = request.url_root.rstrip('/')
        thread = Thread(target=start_send_emails_async, args=(app, [(user['email'], user['id'])], base_url, "emails/microsoft.html"))
        thread.start()

        return redirect("/dashboard")
    return Response("User not found", status=404)
