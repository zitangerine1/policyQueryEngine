from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from vertexconvo import multi_turn_search_sample
from flask_socketio import SocketIO, emit

from google.cloud.sql.connector import Connector
import sqlalchemy
from db import create_db

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

DB_USER = "couch"
DB_PASS = "476913"
DB_NAME = "db1"

# create_db()

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

user_num = 1

@app.route("/")
def landing():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    global user_num
    
    insert_user = sqlalchemy.text("INSERT INTO users (user_id, username, email) VALUES (:user_id, :username, :email)")

    email = request.form.get('email')
    password = request.form.get('password')
    
    """
    LOGIN/IAM is not complete, nor worked on. Please use the below crendentials to login.
    admin@gmail.com, (password: abc)
    a@gmail.com, (password: abc)
    """

    if email == 'admin@gmail.com' and password == 'abc':
        with pool.connect() as db_conn:
            check = db_conn.execute(
                sqlalchemy.text("SELECT * FROM users WHERE email = :email"), {"email": email}
            )
            # check if check is nonetype, if so, create user
            
            try: 
                exists = check.fetchone()[0] #type: ignore
                
            except TypeError:
                exists = False
            
            if not exists: 
                global user_num
                result = db_conn.execute(
                sqlalchemy.text("SELECT MAX(user_id) FROM users")
                )
                max_id = result.fetchone()[0] # type: ignore
                user_num = max_id + 1 if max_id else 1
                
                db_conn.execute(insert_user, parameters={"user_id": user_num, "username": "admin", "email": "admin@gmail.com"})
                db_conn.commit()
                db_conn.close()
        
        session['email'] = email
        return redirect(url_for('index'))
    
    elif email == 'a@gmail.com' and password == 'abc':
        user_num = 2
        with pool.connect() as db_conn:
            check = db_conn.execute(
                sqlalchemy.text("SELECT * FROM users WHERE email = :email"), {"email": email}
            )
            
            try: 
                exists = check.fetchone()[0] #type: ignore
                
            except TypeError:
                exists = False
            
            if not exists:
                result = db_conn.execute(
                sqlalchemy.text("SELECT MAX(user_id) FROM users")
                )
                max_id = result.fetchone()[0] # type: ignore
                user_num = max_id + 1 if max_id else 1
                
                db_conn.execute(insert_user, parameters={"user_id": user_num, "username": "user", "email": "a@gmail.com"})
                db_conn.commit()
                db_conn.close()
            
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
    return render_template('stats.html')


@app.route('/convos')
def pastconv():
    return render_template('convos.html')


conversation_id = 0

@app.route('/sendmessage', methods=["POST"])
def append_dict():
    global conversation_id
    
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

    info, source = multi_turn_search_sample(project_id=project_id, location=location, data_store_id=get_val(), search_queries=search_queries) # type: ignore
    current_res = info[-1] # type: ignore

    insert_stmt = sqlalchemy.text(
        "INSERT INTO conversation (conversation_id, user_id, user_num, timestamp, message, response, datastore) VALUES (:conversation_id, :user_id, :user_num, :timestamp, :message, :response, :datastore)",
    )
    
    store_time = time.strftime('%Y-%m-%d %H:%M:%S')

    conversation_data.append({
        'sender': 'System Message',
        'time': f'{current_time}',
        'message': f'{current_res}',
        'source1': f'{source[0]}', # type: ignore
        'source2': f'{source[1]}', # type: ignore
        'source3': f'{source[2]}'  # type: ignore
    })
    
    with pool.connect() as db_conn:
        result = db_conn.execute(
            sqlalchemy.text("SELECT MAX(conversation_id) FROM conversation")
        )
        max_id = result.fetchone()[0] # type: ignore
        conversation_id = max_id + 1 if max_id else 1

        db_conn.execute(insert_stmt, parameters={"conversation_id": conversation_id, "user_id": user_num, "user_num": user_num, "timestamp": store_time, "message": payload["message"], "response": current_res, "datastore": active_store})
        db_conn.commit()
        db_conn.close()

    socketio.emit('new_message', payload)
    return jsonify(payload), 200


@app.route('/getallmessages', methods=["GET"])
def get_latest_message():
    return jsonify(conversation_data)


@app.route('/getallconvos', methods=["GET"])
def get_all_convos():
    with pool.connect() as db_conn:
        result = db_conn.execute(
            sqlalchemy.text("SELECT * FROM conversation")
        )
        db_conn.close()
        
    return jsonify(result)

with pool.connect() as db_conn:
    result = db_conn.execute(
        sqlalchemy.text("SELECT * FROM users")
    )
    
    for row in result:
        print(row)
        

if __name__ == '__main__':
    socketio.run(debug=True) # type: ignore
