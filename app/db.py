from os import path
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey
    )
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from utility import random_password, hash_password

Base = declarative_base()


class User(Base):
    """
    Database model for the user table.

    Attributes:
        UID (str): The unique identifier of the user.
        Name (str): The name of the user.
        Firstname (str): The first name of the user.
        DOB (Date): The date of birth of the user.
        CA (str): The CA of the user.
        Logins (list): A list of login instances associated with the user.
        Logoffs (list): A list of logoff instances associated with the user.
    """
    __tablename__ = 'user'
    UID = Column(String, primary_key=True)
    Name = Column(String, nullable=False)
    Firstname = Column(String, nullable=False)
    DOB = Column(Date, nullable=False)
    CA = Column(String, ForeignKey('class.CA'))
    Logins = relationship('Login', backref='user', lazy=True)
    Logoffs = relationship('Logoff', backref='user', lazy=True)


class Login(Base):
    """
    Database model for the login table.

    Attributes:
        NR (int): The unique identifier of the login.
        Time (DateTime): The time of the login.
        UID (str): The UID of the user who logged in.
    """
    __tablename__ = 'login'
    NR = Column(Integer, primary_key=True, autoincrement=True)
    Time = Column(DateTime, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Logoff(Base):
    """
    Database model for the logoff table.

    Attributes:
        NR (int): The unique identifier of the logoff.
        Time (DateTime): The time of the logoff.
        UID (str): The UID of the user who logged off.
    """
    __tablename__ = 'logoff'
    NR = Column(Integer, primary_key=True, autoincrement=True)
    Time = Column(DateTime, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Admin(Base):
    """
    Database model for the admin table.

    Attributes:
        Username (str): The username of the admin.
        Password (str): The password of the admin.
        UID (str): The UID of the corresponding User.
    """
    __tablename__ = 'admin'
    Username = Column(String, primary_key=True)
    Password = Column(String, nullable=False)
    UID = Column(String, ForeignKey('user.UID'))


class Class(Base):
    """
    Database model for the class table.

    Attributes:
        CA (str): The CA of the class.
        Subject_area (str): The subject area of the class.
        Classroom (str): The classroom of the class.
        Students (list): A list of user instances associated with the class.
    """
    __tablename__ = 'class'
    CA = Column(String, primary_key=True)
    Subject_area = Column(String, nullable=False)
    Classroom = Column(String, nullable=False)
    Students = relationship('User', backref='class', lazy=True)


def init_db(db_url: str):
    """
    Initializes the database.

    Args:
        db_url (str): The URL of the database.
    """
    engine = create_engine(db_url)
    # Tabellen erstellen
    Base.metadata.create_all(engine)
    # Session erstellen
    Session = sessionmaker(bind=engine)
    session = Session()

    # Beispiel-Datensatz hinzufügen
    rndpw = random_password()
    master_admin = Admin(Username='master', Password=hash_password(rndpw))
    session.add(master_admin)
    session.commit()
    print(f"Master-Admin added. Note the Password: {rndpw}")
    print("## You won't see it again. Please note the password. ##")


if __name__ == '__main__':
    basedir = path.abspath(path.dirname(__file__))
    init_db('sqlite:///' + path.join(basedir, 'db/database.db'))
