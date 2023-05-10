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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """POST /sessions route."""
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """DELETE /sessions route."""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = User.get(session_token=session_id)
    if not user:
        abort(403)

    user.delete_session(session_id)
    response = make_response(redirect('/'))
    response.set_cookie('session_id', expires=0)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
