from app import create_app
from config import PRODUCTION, PORT
import logging

app = create_app()

if __name__ == "__main__":
    logging.basicConfig(filename="logs/app.log", level=logging.INFO)
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=not PRODUCTION
    )