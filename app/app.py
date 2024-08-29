from os import path
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db import init_db, Admin, User, Class, Login, Logoff
from utility import hash_password, verify_password

server = Flask(__name__)

# Database initialization
basedir = path.abspath(path.dirname(__file__))
path2db = path.join(basedir, 'db/database.db')
sqpath = 'sqlite:///' + path.join(basedir, 'db/database.db')

if not path.exists(path.join(basedir, 'db/database.db')):
    print("Database not generated. Generating database")
    init_db(sqpath)

# Database configuration
server.config['SQLALCHEMY_DATABASE_URI'] = sqpath
db = SQLAlchemy(server)


@server.route("/")
def index():
    return render_template("index.html")


# Remove second route and default value for production !!
@server.route("/user_test")
@server.route("/user_<userid>")
def user(userid: str = "test"):
    """User Page to start logging Time

    Args:
        userid (str): Needs to be given to load User Data! Defaults to test for DEV

        !!REMOVE SECOND ROUTE AND DEFAULT VALUE FOR PRODUCTION!!

    Returns:
        Page: User Page
    """
    return render_template("user.html",
                           logins={},
                           logouts={},
                           user={"firstname": "John",
                                 "name": "Doe",
                                 "image": url_for("static",
                                                  filename="images/placeholder_user.svg")})


if __name__ == "__main__":
    server.run("0.0.0.0", "5005", debug=True)
