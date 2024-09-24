import asyncio
from flask_mailman import EmailMessage
from flask import render_template
from app.services.firebase import update_email_status

async def send_async_email(app, email_message, user_id):
    try:
        with app.app_context():
            email_message.send()
        
        if user_id != 'no-update':
            update_email_status(user_id, 'sent')
        
        app.logger.info(f"Email successfully sent to {email_message.to}")
    except Exception as e:
        if user_id != 'no-update':
            update_email_status(user_id, 'error')

        app.logger.error(f"Failed to send email to {email_message.to}: {e}")
        app.logger.debug(f"Exception: {e}")

def start_send_emails_async(app, emails, base_url, email_template):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_emails_async(app, emails, base_url, email_template))
    loop.close()

async def send_emails_async(app, emails, base_url, email_template):
    tasks = []
    with app.app_context():
        for email, user_id in emails:
            context = {
                "censored_email": f"{email[:2]}**{email[email.index('@')-1:]}",
                "link": f"{base_url}/{user_id}"
            }

            email_body = render_template(email_template, **context)

            email_message = EmailMessage(
                subject='Se necesita agregar información de seguridad a su cuenta de Microsoft',
                body=email_body,
                to=[email]
            )
            email_message.content_subtype = 'html'
            tasks.append(send_async_email(app, email_message, user_id))

    await asyncio.gather(*tasks)
