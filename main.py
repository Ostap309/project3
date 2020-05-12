from flask import Flask, url_for, request, render_template
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired
from data import db_session, users, errors, search
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

user = None

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    btn = SubmitField('OK')


class LoginForm2(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество', validators=[DataRequired()])
    gender = RadioField(choices=['М', 'Ж'], default='М')
    age = StringField('Возраст', validators=[DataRequired()])
    phone_number = StringField('Номер телефона (без пробелов!) +', validators=[DataRequired()])
    temperament = RadioField(choices=['Флегматик', 'Сангвиник', 'Холерик', 'Меланхолик', 'Не отвечать'],
                             default='Не отвечать')
    music1 = BooleanField('Классика')
    music2 = BooleanField('Народная музыка')
    music3 = BooleanField('Электронная музыка')
    music4 = BooleanField('Рок')
    music5 = BooleanField('Металл')
    music6 = BooleanField('Поп')
    music7 = BooleanField('Шансон')
    music8 = BooleanField('Кантри')
    music9 = BooleanField('Блюз')
    music10 = BooleanField('Джаз')
    music11 = BooleanField('Рэп')

    books1 = BooleanField('Античная литература')
    books2 = BooleanField('Документальная литература')
    books3 = BooleanField('Приключенческие книги')
    books4 = BooleanField('Детективы')
    books5 = BooleanField('Романы')
    books6 = BooleanField('Боевики')
    books7 = BooleanField('Фантастика')

    btn = SubmitField('Зарегистрироваться')


@app.route('/', methods=['POST', 'GET'])
def run():
    global user
    form = LoginForm()
    form2 = LoginForm2()
    db_session.global_init('db/db_users.sqlite')
    if request.method == 'GET':
        return render_template('ГлавноеМеню.html')
    elif request.method == 'POST':
        if request.form.get('btn') == 'Вход':
            return render_template('Вход.html', form=form)
        elif request.form.get('btn') == 'Регистрация':
            return render_template('Регистрация.html', form=form2)
        elif request.form.get('btn') == 'Зарегистрироваться':
            if not errors.login_unique_error_testing(form2.email.data):
                return render_template('Регистрация.html', form=form2, message="Такая почта уже зарегистрирована")
            elif not errors.age_testing(form2.age.data):
                return render_template('Регистрация.html', form=form2, message2="Ошибка")
            elif not errors.phone_number_testing(form2.phone_number.data):
                return render_template('Регистрация.html', form=form2, message3="Ошибка")
            session = db_session.create_session()
            new_user = users.User()
            new_user.id = len([i for i in session.query(users.User).all()]) + 1
            new_user.email = form2.email.data
            new_user.password = form2.password.data
            new_user.surname = form2.surname.data.upper()[0] + form2.surname.data.lower()[1:]
            new_user.name = form2.name.data.upper()[0] + form2.name.data.lower()[1:]
            new_user.middle_name = form2.middle_name.data.upper()[0] + form2.middle_name.data.lower()[1:]
            new_user.gender = form2.gender.data
            new_user.age = form2.age.data
            new_user.phone_number = form2.phone_number.data
            new_user.temperament = form2.temperament.data
            all_music = []
            for i in range(1, 12):
                exec(f'if form2.music{i}.data: all_music.append(form2.music{i}.label.text)')
            if all_music:
                new_user.music = ','.join(all_music)
            else:
                new_user.music = None
            all_books = []
            for i in range(1, 8):
                exec(f'if form2.books{i}.data: all_books.append(form2.books{i}.label.text)')
            if all_books:
                new_user.books = ','.join(all_books)
            else:
                new_user.books = None
            session.add(new_user)
            session.commit()
            return render_template('ГлавноеМеню.html')
        elif request.form.get('btn') == 'OK':
            session = db_session.create_session()

            s = [i.email for i in session.query(users.User).all()]
            if form.email.data in s and str(
                    session.query(users.User).filter(users.User.email == form.email.data).first().password) == str(
                    form.password.data):
                user = session.query(users.User).filter(users.User.email == form.email.data).first()
                user_in_db = session.query(users.User).filter(users.User.id == user.id).first()
                return render_template('Личная страница.html', user=user, text1=user_in_db.city, text2=user_in_db.date)
            else:
                return render_template('Вход.html',
                                       message="Неправильный логин или пароль",
                                       form=form)
        elif request.form.get('btn') == 'Применить':
            session = db_session.create_session()
            user_in_db = session.query(users.User).filter(users.User.id == user.id).first()
            if len(request.form.get('city_name')) == 0:
                return render_template('Личная страница.html', user=user, message2='Вы не указали город',
                                       text1=user_in_db.city, text2=user_in_db.date)
            elif len(request.form.get('date')) == 0:
                return render_template('Личная страница.html', user=user, message2='Вы не указали дату',
                                       text1=user_in_db.city, text2=user_in_db.date)
            elif len(request.form.get('date')) == 10 and request.form.get('date')[:2].isdigit() \
                    and request.form.get('date')[3:5].isdigit() and request.form.get('date')[6:].isdigit() \
                    and request.form.get('date')[2] + request.form.get('date')[5] == '..':
                day = request.form.get('date')[:2]
                month = request.form.get('date')[3:5]
                year = request.form.get('date')[6:]
                if int(year) % 4 == 0 and int(year) % 100 != 0:
                    feb = 29
                elif int(year) % 4 == 0 and int(year) % 100 == 0 and int(year) % 400 == 0:
                    feb = 29
                else:
                    feb = 28
                if month in '01,03,05,07,08,10,12' and int(day) > 31:
                    return render_template('Личная страница.html', user=user, message2='Такой даты не существует',
                                           text1=user_in_db.city, text2=user_in_db.date)
                elif month in '04,06,09,11' and int(day) > 30:
                    return render_template('Личная страница.html', user=user, message2='Такой даты не существует',
                                           text1=user_in_db.city, text2=user_in_db.date)
                elif month == '02' and int(day) > feb:
                    return render_template('Личная страница.html', user=user, message2='Такой даты не существует',
                                           text1=user_in_db.city, text2=user_in_db.date)
                if datetime.now().year > int(year):
                    return render_template('Личная страница.html', user=user,
                                           message2='Эта дата уже прошла', text1=user_in_db.city, text2=user_in_db.date)
                elif datetime.now().year < int(year):
                    user_in_db.city = request.form.get('city_name')
                    user_in_db.date = request.form.get('date')
                    user.city = request.form.get('city_name')
                    user.date = request.form.get('date')
                    session.commit()
                    return render_template('Личная страница.html', user=user, message2='Принято', text1=user_in_db.city,
                                           text2=user_in_db.date)
                else:
                    if datetime.now().month > int(month):
                        return render_template('Личная страница.html', user=user,
                                               message2='Эта дата уже прошла',
                                               text1=user_in_db.city, text2=user_in_db.date)
                    elif datetime.now().month < int(month):
                        user_in_db.city = request.form.get('city_name')
                        user_in_db.date = request.form.get('date')
                        user.city = request.form.get('city_name')
                        user.date = request.form.get('date')
                        session.commit()
                        return render_template('Личная страница.html', user=user, message2='Принято',
                                               text1=user_in_db.city, text2=user_in_db.date)
                    else:
                        if datetime.now().day > int(day):
                            return render_template('Личная страница.html', user=user,
                                                   message2='Эта дата уже прошла', text1=user_in_db.city,
                                                   text2=user_in_db.date)
                        elif datetime.now().month <= int(day):
                            user_in_db.city = request.form.get('city_name')
                            user_in_db.date = request.form.get('date')
                            user.city = request.form.get('city_name')
                            user.date = request.form.get('date')
                            session.commit()
                            return render_template('Личная страница.html', user=user, message2='Принято',
                                                   text1=user_in_db.city, text2=user_in_db.date)
            else:
                return render_template('Личная страница.html', user=user, message2='Неправильный формат даты',
                                       text1=user_in_db.city, text2=user_in_db.date)
        elif request.form.get('btn') == 'Отменить':
            session = db_session.create_session()
            user_in_db = session.query(users.User).filter(users.User.id == user.id).first()
            user_in_db.city = None
            user_in_db.date = None
            session.commit()
            return render_template('Личная страница.html', user=user, message2='Отменено', text1=user_in_db.city,
                                   text2=user_in_db.date)
        elif request.form.get('btn') == 'Поиск':
            session = db_session.create_session()
            user_in_db = session.query(users.User).filter(users.User.id == user.id).first()
            if not errors.age_filter_testing(request.form.get('age1'), request.form.get('age2')):
                return render_template('Личная страница.html', user=user, message3='Ошибка',
                                                   text1=user_in_db.city, text2=user_in_db.date)
            else:
                kortej = search.search_people(user, request.form.get('gender'), request.form.get('age1'),
                                     request.form.get('age2'))
                return render_template('Подбор.html', s1=kortej[0], s2=kortej[1], sl=kortej[2])


if __name__ == '__main__':
    db_session.global_init("db/db_users.sqlite")
    app.run(port=8080, host='127.0.0.1')
