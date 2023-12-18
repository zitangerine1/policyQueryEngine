from flask import Flask, render_template, request, redirect, url_for, session, flash
# from vertexcall import search_sample
import time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

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
    conversation_data = [
        {
            'sender': 'User',
        },
        {
            'sender': 'User',
            'time': f'{current_time}',
            'message': f'Hello!'
        },
        {
            'sender': 'System Message',
            'time': f'{current_time}',
            'message': f'Hello, how are you?'
        },
        {
            'sender': 'User',
            'time': f'{current_time}',
            'message': f'Good.'
        },
        {
            'sender': 'System Message',
            'time': f'{current_time}',
            'message': f'Amazing.'
        },
        {
            'sender': 'User',
            'time': f'{current_time}',
            'message': f'Good.'
        },
    ]

    if len(conversation_data) > 6:
        conversation_data.pop(2)

    # info = search_sample()
    email = session.get('email')
    return render_template("index.html", email=email, conversation_data=conversation_data)


if __name__ == '__main__':
    app.run(debug=True)
    
    