from flask import Flask
import psycopg2

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello via docker"


@app.route("/initdatabase")
def db_init():
    # if module is imported use the localhost
    db_host = "my_postgres"

    connection = psycopg2.connect(host=db_host, user="postgres", password="passw0rd")
    connection.set_isolation_level(0)  # else cannot drop a db in a trxn
    cursor = connection.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    connection = psycopg2.connect(
        host=db_host, user="postgres", password="passw0rd", database="inventory"
    )

    connection.set_isolation_level(0)  # else cannot drop a db in a trxn
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return "init database"


@app.route("/addwidget")
def add_widget():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0")
