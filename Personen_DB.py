from Personen_abc import Person, Customer, Randomize_Names
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length

""" Database """

db = SQLAlchemy()

class Person_DB(db.Model):
    __tablename__ = "Personen v1"
    # mandatory values.
    id = db.Column(db.Integer, primary_key = True, nullable = False)
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

def Find_Person_ID(id):
    return Person_DB.query.filter_by(id=id).first()

def Find_Person_Name(name):
    return Person_DB.query.filter_by(name=name).first()

def Personify_from_Form(form):
    name = form.get("name")
    app.logger.info(f"Personifying: {name}")
    customer_id = db.session.query(Person_DB).count() +1
    return Person_DB(id = customer_id, name = form.get("name"), birthday=form.get("birthday"), city=form.get("city"), email=form.get("email"), phone=form.get("phone"))


""" App """

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

    """ Forms """

    class AddPersonForm(FlaskForm):
            name = StringField("Name: ", validators=[InputRequired(), Length(min=1, max=100)])
            birthday = StringField("Birthday: ", validators=[InputRequired(), Length(min=1, max=100)])
            city = StringField("City: ", validators=[InputRequired(), Length(min=1, max=100)])
            email = StringField("Email: ", validators=[InputRequired(), Length(min=1, max=100)])
            phone = StringField("Phone: ", validators=[InputRequired(), Length(min=1, max=100)])
            submit = SubmitField("Add")

    class FindPersonForm(FlaskForm):
        option = SelectField('Reference: ', choices=[('id','ID'),('name','Name')])
        query = StringField("Query:", validators=[InputRequired(), Length(min=1, max=100)])
        submit = SubmitField("Go")

    """ Webpages """

    @app.route("/base", methods=["POST", "GET"])
    def base():
        # base page and db.
        app.logger.info("Base")
        daba_entries = db.session.query(Person_DB).all()
        return render_template("db_base.html", person_table = daba_entries)

    @app.route("/base/add", methods=["POST", "GET"])
    def add_person():
        app.logger.info("adding person")
        add_link_form = AddPersonForm()
        if request.method == "POST":
            person_add = Personify_from_Form(request.form)
            db.session.add(person_add)
            db.session.commit()
            app.logger.info("Adding completed.")
            return render_template("add_person.html", form = add_link_form, heading = "Added Person to DB.")

        return render_template("add_person.html", form = add_link_form, heading = "Enter your Name.")

    def Return_Person_str(person: Person_DB):
        return f"{person.id}:{person.name}:{person.email}:{person.phone}"

    @app.route("/base/find", methods = ["POST", "GET"])
    def find_person():
        app.logger.info("finding person")
        find_form = FindPersonForm()
        if request.method == "POST":
            option_find = request.form.get("option")
            if option_find == "id":
                person = Find_Person_ID(request.form.get("query"))
            else:
                person = Find_Person_Name(request.form.get("query"))
            
            return render_template("find_person.html", form = find_form, heading = Return_Person_str(person))
        return render_template("find_person.html", form = find_form, heading = "Find Person")

    return app


if __name__ == "__main__":
    app = Create_App()
    app.run(debug=True)
    print("-----> http://127.0.0.1:5000/base ")
    print("-----> http://127.0.0.1:5000/base/add ")

