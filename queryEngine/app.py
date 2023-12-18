from flask import Flask, render_template, request, redirect, url_for, session, flash
from vertexcall import search_sample

# from dotenv import load_dotenv
# import os

# load_dotenv("./secret.env")
app = Flask(__name__)
app.secret_key = "9irrqyjcn595lmnf7zsl19xbig3bhaqb"

@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    isAuth = False
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email == 'admin@mindef.com' and password == 'abc':
        isAuth = True
        # Redirect to the success page if authentication is successful
        session['email'] = email
        return redirect(url_for('index'))
    else:
        flash('Incorrect email or password. Please try again.', 'Error: ')
        return render_template("login.html")
    

@app.route("/chat")
def index():
    email = session.get('email')
    return render_template("index.html", email=email)


if __name__ == '__main__':
    app.run(debug=True)
    
    