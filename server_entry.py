# server_entry.py
import os, socket, webbrowser, sys
from uvicorn import Config, Server

# IMPORTANT: make sure "app" is importable when frozen
# If PyInstaller changes CWD, adjust sys.path to project dir:
BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from app.main import app  # after path fix

def get_free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

if __name__ == "__main__":
    port = int(os.environ.get("PORT", get_free_port()))
    host = "0.0.0.0"

    # Write a helper URL + open the browser for non-tech users
    url = f"http://localhost:{port}/"
    try:
        with open(os.path.join(BASE, "server-url.txt"), "w", encoding="utf-8") as f:
            f.write(url + "\n")
        # Open landing page
        webbrowser.open(url)
    except Exception:
        pass

    Server(Config(app=app, host=host, port=port, log_level="info")).run()
