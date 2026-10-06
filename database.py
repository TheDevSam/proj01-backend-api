import os
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database="posts_app"
    )