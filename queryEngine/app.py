from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from vertexconvo import multi_turn_search_sample
from flask_socketio import SocketIO, emit

from google.cloud.sql.connector import Connector
import sqlalchemy

connector = Connector()


def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn


pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

INSTANCE_CONNECTION_NAME = "policy-query-engine:us-west1:response-database"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")

DB_USER = "couch"
DB_PASS = "476913"
DB_NAME = "users"

with pool.connect() as db_conn:
    db_conn.execute(
        sqlalchemy.text(
            "CREATE TABLE IF NOT EXISTS users "
            "( user_id INT PRIMARY KEY, "
            "username VARCHAR(255) NOT NULL, "
            "email VARCHAR(255) NOT NULL);"
        )
    )

    db_conn.commit()

    insert_stmt = sqlalchemy.text(
        "INSERT INTO users (username, email) VALUES (:username, :email)",
    )

    

# -- Local TODOs --
# TODO: Source listing
# TODO: Loading animation
# TODO: Datastore selection
# TODO: IAM + SQL Testing

# -- After production ready --
# TODO: CloudSQL + Cloud Run

import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

conversation_data = []
source_data = []

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
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = "9irrqyjcn595lmnf7zsl19xbig3bhaqb"


@app.route("/")
def landing():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == 'admin@gmail.com' and password == 'abc':
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

    socketio.emit("user_message")

    active_store: str = "google"

    def get_val():
        for store in datastores:
            if active_store in store:
                return store[active_store]

    print(search_queries)

    info, source = multi_turn_search_sample(project_id=project_id, location=location, data_store_id=get_val(),
                                            search_queries=search_queries)

    conversation_data.append({
        'sender': 'System Message',
        'time': f'{current_time}',
        'message': f'{info.pop()}',
        'source1': f'{source[0]}',
        'source2': f'{source[1]}',
        'source3': f'{source[2]}'
    })

    socketio.emit('new_message', payload)
    return jsonify(payload), 200


@app.route('/getallmessages', methods=["GET"])
def get_latest_message():
    return jsonify(conversation_data)


if __name__ == '__main__':
    socketio.run(debug=True)
