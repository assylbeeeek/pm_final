from flask import Flask, render_template, request, flash, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

db = SQLAlchemy()
bcrypt = Bcrypt()


app = Flask(__name__)

app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# login_manager.init_app(app)
db.init_app(app)
bcrypt.init_app(app)

b = False


login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iin = db.Column(db.String(12), unique=True, nullable=False)
    full_name = db.Column(db.String(300), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(300), nullable=False)
    languages = db.Column(db.String(300), nullable=True)
    birth_place = db.Column(db.String(300), nullable=True)
    birth_date = db.Column(db.String(300), nullable=True)
    education = db.Column(db.String(300), nullable=True)
    nationality = db.Column(db.String(300), nullable=False)
    martial_status = db.Column(db.String(300), nullable=True)
    amount_of_children = db.Column(db.Integer, nullable=True)
    p_number = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.full_name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    global b
    if b:
        b = False
        return render_template('Main.html', title='Bureau', message="Congratulations, you complete survey!")
    return render_template('Main.html', title='Bureau')


@app.route('/', methods=['POST'])
def index_post():
    return redirect(url_for('iin'))


@app.route('/iin', methods=['GET'])
def iin():
    return render_template('IIN.html', title='Bureau')


@app.route('/iin', methods=['POST'])
def iin_post():
    global iin_temp
    iin_temp = request.form['iin']
    if len(iin_temp) == 12 and not User.query.filter_by(iin=iin_temp).first():
            return redirect((url_for('survey')))
    flash('This iin already passed this survey or iin not 12 length' + iin_temp)
    return redirect(url_for('iin'))


@app.route('/survey', methods=['GET'])
def survey():
    return render_template('Register.html', title='Survey by National Statistics Bureau')


@app.route('/survey', methods=['POST'])
def survey_post():
    f_name = request.form['first_name']
    s_name = request.form['second_name']
    l_name = request.form['last_name']
    age = int(request.form['age'])
    gender = request.form['gender']
    languages = request.form['languages']
    birth_place = request.form['birth_place']
    birth_date = request.form['birth_date']
    education = request.form['education']
    nationality = request.form['nationality']
    martial_status = request.form['martial_status']
    amount_of_children = request.form['amount_of_children']
    p_number = request.form['phone_number']

    if f_name == "":
        flash('First Name is empty')
        return redirect(url_for('survey'))
    if s_name == "":
        flash('Second Name is empty')
        return redirect(url_for('survey'))
    if l_name == "":
        flash('Last Name is empty')
        return redirect(url_for('survey'))
    if age == 0:
        flash('Age is empty')
        return redirect(url_for('survey'))
    if gender == "":
        flash('Gender is empty')
        return redirect(url_for('survey'))
    if nationality == "":
        flash('Nationality is empty')
        return redirect(url_for('survey'))

    if amount_of_children:
        amount_of_children = int(amount_of_children)

    full_name = f_name + " " + s_name + " " + l_name
    global iin_temp

    user = User(iin=iin_temp, full_name=full_name, age=age, gender=gender, languages=languages, birth_place=birth_place,
                birth_date=birth_date, education=education, nationality=nationality, martial_status=martial_status, amount_of_children=amount_of_children,
                p_number=p_number)
    db.session.add(user)
    db.session.commit()
    global b
    b = True
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)