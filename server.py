from flask import Flask, url_for, request, render_template, json, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from data import db_session, users, jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    user_id = StringField('Id астронавта', validators=[DataRequired()])
    user_password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_username = StringField('Id капитана', validators=[DataRequired()])
    cap_password = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    age = IntegerField('Возраст')
    position = StringField('Должность пользователя', validators=[DataRequired()])
    speciality = StringField('Специализация пользователя', validators=[DataRequired()])
    address = StringField('Адрес пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


def view_job():
    job_list = []
    db_session.global_init("db/mars_explorer.sqlite")
    session = db_session.create_session()
    for job_elem in session.query(jobs.Job).all():
        user = session.query(users.User).filter(users.User.id == job_elem.team_leader).first()
        job_list.append(
            [job_elem.job, f'{user.surname} {user.name}', job_elem.work_size,
             job_elem.collaborators,
             job_elem.is_finished])
    return job_list


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form,
                           css_file=url_for('static', filename='css/style.css'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    params = dict()
    params['form'] = form
    params['image'] = url_for('static', filename='img/MARS.png')
    params['title'] = 'Авторизация'
    params['css_file'] = url_for('static', filename='css/style.css')
    return render_template('login.html', **params)


@app.route('/index/<title>')
def index(title):
    params = dict()
    params['title'] = title
    params['css_file'] = url_for('static', filename='css/style.css')
    return render_template('base.html', **params)


@app.route('/training/<prof>')
def training(prof):
    return render_template('prof.html', image_inj=url_for('static', filename='img/инжинер.jpg'), prof=prof,
                           image_other=url_for('static', filename='img/другой.jpg'),
                           css_file=url_for('static', filename='css/style.css'))


@app.route('/list_prof/<type_list>')
def list_prof(type_list):
    params = dict()
    params['css_file'] = url_for('static', filename='css/style.css')
    params['title'] = 'Список профессий'
    params['type_list'] = type_list
    return render_template('list.html', **params)


@app.route('/auto_answer')
@app.route('/answer')
def answer():
    params = dict()
    params['title'] = 'Анкета'
    params['css_file'] = url_for('static', filename='css/style.css')
    params['surname'] = 'Wanty'
    params['name'] = 'Mark'
    params['education'] = 'выше среднего'
    params['profession'] = 'штурман марсохода'
    params['sex'] = 'male'
    params['motivation'] = 'Мечатю умереть на Марсе!'
    params['ready'] = True
    return render_template('auto_answer.html', **params)


@app.route('/distribution')
def distribution():
    params = dict()
    params['css_file'] = url_for('static', filename='css/style.css')
    params['user_list'] = list(["Aфыв", 'Bфыв', 'C', 'Dы', 'E'])
    return render_template('cabins.html', **params)


@app.route('/table/<sex>/<int:year>')
def table(sex, year):
    params = dict()
    params['css_file'] = url_for('static', filename='css/style.css')
    if sex == 'male':
        if year < 21:
            params['emblem_color'] = url_for('static', filename='img/male_emblem.jpg')
            params['wall_color'] = url_for('static', filename='img/low_blue.jpg')
        else:
            params['emblem_color'] = url_for('static', filename='img/big_male_emblem.jpg')
            params['wall_color'] = url_for('static', filename='img/blue.jpg')
    elif sex == 'female':
        if year < 21:
            params['emblem_color'] = url_for('static', filename='img/female_emblem.jpg')
            params['wall_color'] = url_for('static', filename='img/low_purple.jpg')
        else:
            params['emblem_color'] = url_for('static', filename='img/big_female_emblem.jpg')
            params['wall_color'] = url_for('static', filename='img/purple.jpg')
    return render_template('table.html', **params)


@app.route('/list_jobs')
def list_jobs():
    params = dict()
    params['css_file'] = url_for('static', filename='css/style.css')
    params['job_list'] = view_job()
    return render_template('jobs.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
