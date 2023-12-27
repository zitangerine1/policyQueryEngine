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

DB_USER = "couch"
DB_PASS = "476913"
DB_NAME = "db1"

def create_db():
    with pool.connect() as db_conn:
        db_conn.execute(
            sqlalchemy.text(
                "CREATE TABLE IF NOT EXISTS users "
                "( user_id INT PRIMARY KEY, "
                "username VARCHAR(255) NOT NULL, "
                "email VARCHAR(255) NOT NULL);"
            )
        )

        db_conn.execute(
            sqlalchemy.text(
                "CREATE TABLE IF NOT EXISTS conversation"
                "( conversation_id INT PRIMARY KEY, "
                "user_id INT, "
                "user_num INT, "
                "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                "message TEXT, "
                "response TEXT, "
                "datastore TEXT, "
                "FOREIGN KEY (user_id) REFERENCES users(user_id));"
            )
        )

        db_conn.commit()
        db_conn.close()

# purge_dbs()
create_db()

# # show rows of all tables

# with pool.connect() as db_conn:
#     result = db_conn.execute(
#         sqlalchemy.text("SELECT * FROM conversation")
#     )
    
#     for row in result:
#         print(row)
        
#     db_conn.close()
        
# with pool.connect() as db_conn:
#     result = db_conn.execute(
#         sqlalchemy.text("SELECT * FROM users")
#     )
    
#     for row in result:
#         print(row)
        
#     db_conn.close()