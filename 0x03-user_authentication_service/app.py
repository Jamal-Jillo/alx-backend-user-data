#!/usr/bin/env python3
"""Simple Flask app, basic authentication."""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def home():
    """Home endpoint."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
