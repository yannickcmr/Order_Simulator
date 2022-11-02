from Personen_abc import Person, Customer, Randomize_Names
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length

db = SQLAlchemy()

class Person_DB(db.Model):
    __tablename__ = "Personen v1"
    # mandatory values.
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    birthday = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    # optional values, will be added if order has been placed.
    last_order_id = db.Column(db.Integer)
    mean_volume = db.Column(db.Integer)
    mean_order_value = db.Column(db.Integer)
    mean_item_count = db.Column(db.Integer)

    def Find_Person_ID(self, id):
        pass

    def Find_Person_Name(self, name):
        pass

    def Add_Person(self, person: Person):
        app.logger.info(f"adding: {person.name}")

def Create_App():
    # App config.
    app = Flask(__name__)
    CORS(app, send_wildcard=True)
    app.secret_key = "test1234"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        # initialize db
        db.create_all()

    @app.route("/base", methods=["POST", "GET"])
    def base():
        # base page and db.
        app.logger.info("Base")
        daba_entries = Person_DB.query.all()
        return render_template("db_base.html", person_table = daba_entries)

    return app


if __name__ == "__main__":
    app = Create_App()
    app.run(debug=True)
    print("-----> http://127.0.0.1:5000/base ")

    test = Randomize_Names("Person.csv", 1)[0]
    db.session.Add_Person(Person_DB, test)

