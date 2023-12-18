from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from vertexcall import search_sample
import time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

conversation_data = []

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
    active_stores = []
    # info = search_sample()
    email = session.get('email')
    return render_template("index.html", email=email, conversation_data=conversation_data)


@app.route('/statistics')
def stats():
    return render_template('update_content.html')


@app.route('/convos')
def pastconv():
    return render_template('convos.html')


@app.route('/sendmessage', methods=["POST"])
def append_dict():
    payload = request.get_json()
    conversation_data.append(payload)
    updated_content = render_template('update_content.html', conversation_data=conversation_data)
    print(f'updated_content: {updated_content}')
    return jsonify({'updated_content': updated_content, 'success': True})


if __name__ == '__main__':
    app.run(debug=True)
    
    