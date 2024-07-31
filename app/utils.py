import socket
import user_agents
from flask import request  # Asumiendo que estás usando Flask

def collect_user_info(request):
    # Obtener información del user agent y otros datos
    user_agent_string = request.headers.get('User-Agent', 'unknown')
    
    print("###################")
    for key, value in request.headers.items():
        print(f"{key}: {value}")
    print("###################")

    user_ip = request.headers.get("True-Client-Ip") or \
              request.headers.getlist("X-Forwarded-For")[0] or \
              request.remote_addr

    try:
        user_host = socket.gethostbyaddr(user_ip)[0]
    except socket.herror:
        user_host = 'unknown'

    full_path = request.full_path if hasattr(request, 'full_path') else 'unknown'
    referer = request.headers.get('Referer', 'unknown')
    accept_languages = request.headers.get('Accept-Language', 'unknown')

    # Parsear el user agent
    ua = user_agents.parse(user_agent_string)
    browser = ua.browser.family
    browser_version = ua.browser.version_string
    os = ua.os.family
    os_version = ua.os.version_string
    device = ua.device.family

    print(f"User Agent: {user_agent_string}")
    print(f"User IP: {user_ip}")
    print(f"User Host: {user_host}")
    print(f"Full Path: {full_path}")
    print(f"Referer: {referer}")
    print(f"Accept Languages: {accept_languages}")
    print(f"Browser: {browser}")
    print(f"Browser Version: {browser_version}")
    print(f"OS: {os}")
    print(f"OS Version: {os_version}")
    print(f"Device: {device}")

    # Estructurar los datos para Firebase
    user_data = {
        "user_agent": user_agent_string,
        "user_ip": user_ip,
        "user_host": user_host,
        "full_path": full_path,
        "referer": referer,
        "accept_languages": accept_languages,
        "browser": browser,
        "browser_version": browser_version,
        "os": os,
        "os_version": os_version,
        "device": device
    }

    return user_data
