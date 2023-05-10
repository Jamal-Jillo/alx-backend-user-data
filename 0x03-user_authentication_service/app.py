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


@app.route('/users', methods=['POST'])
def users():
    """POST /users route."""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': user.email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
