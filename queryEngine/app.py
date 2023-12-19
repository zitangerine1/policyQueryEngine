from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from vertexconvo import multi_turn_search_sample
import time
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

conversation_data = []
project_id = "policy-query-engine"
location = "global"

datastores = [
    {"google": "google-policies_1702712626667"},
    {"azure": "azure-policies_1702961323663"},
    {"amazon": "amazon-policies_1702961252887"}
]

search_queries = []

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
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email == 'admin@mindef.com' and password == 'abc':
        # Redirect to the success page if authentication is successful
        session['email'] = email
        return redirect(url_for('index'))
    else:
        flash('Incorrect email or password. Please try again.', 'Error: ')
        return render_template("login.html")
    

@app.route("/chat")
def index():
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
    search_queries.append(payload["message"])

    active_store: str = "google"

    def get_val():
        for store in datastores:
            if active_store in store:
                return store[active_store]

    print(search_queries)

    info = multi_turn_search_sample(project_id=project_id, location=location, data_store_id=get_val(), search_queries=search_queries)
    print(info)

    conversation_data.append({
        'sender': 'System Message',
        'time': f'{current_time}',
        'message': f'{info.pop()}'
    })

    updated_content = render_template('update_content.html', conversation_data=conversation_data)
    return jsonify({'updated_content': updated_content, 'success': True})


if __name__ == '__main__':
    app.run(debug=True)
    
    