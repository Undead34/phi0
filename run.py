from dotenv import load_dotenv
from app import create_app

load_dotenv(override=True)

app = create_app()

if __name__ == '__main__':
    app.run("0.0.0.0", 3000, debug=False)
