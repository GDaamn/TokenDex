"""Serve TokenDex's frontend through the same Python entry point on Docker and Render."""

from pathlib import Path

from flask import Flask, Response, send_from_directory

STATIC_DIR = Path(__file__).resolve().parent / "static"
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")


@app.get("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html", max_age=0)


@app.get("/fonts/<filename>")
def font_asset(filename):
    return send_from_directory(STATIC_DIR / "fonts", filename)


@app.get("/healthz")
def health():
    return Response("ok", mimetype="text/plain")


@app.after_request
def fresh_html(response):
    if response.mimetype == "text/html":
        response.headers["Cache-Control"] = "no-cache"
    return response
