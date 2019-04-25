from flask import Flask, render_template, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import DataBase, ActorsModel, PerformancesModel, UsersModel
from forms import LoginForm, RegistrationForm, PerformanceForm, ActorForm
import datetime


ADMIN_NAME, ADMIN_PASSWORD_HASH = 'admin', generate_password_hash('admin123')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        users_model = UsersModel(db.get_connection())
        exists = users_model.exists(username)
        if exists[0] and check_password_hash(exists[2], password):
            session['username'] = username
            session['user_id'] = exists[1]
            return redirect('/performances')
        return render_template('login.html', title='Авторизация', form=form,
                               error_text='Неверный логин или пароль')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        users_model = UsersModel(db.get_connection())
        for user in users_model.get_all():
            if user[1] == username:
                return render_template('registration.html', title='Регистрация', form=form,
                                       error_text='Этот логин уже занят')
        if len(password1) < 5:
            return render_template('registration.html', title='Регистрация', form=form,
                                   error_text='Пароль слишком короткий')
        elif password1 != password2:
            return render_template('registration.html', title='Регистрация', form=form,
                                   error_text='Пароли различаются')
        else:
            users_model.insert(username, generate_password_hash(password1))
            return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/performances')
def show_performances():
    if 'username' not in session:
        return redirect('/login')
    performances_model = PerformancesModel(db.get_connection())
    performances = performances_model.get_all()
    if session['username'] == ADMIN_NAME:
        admin = True
    else:
        admin = False
    res = {}
    users_model = UsersModel(db.get_connection())
    for item in performances:
        if str(item[0]) in users_model.get(session['user_id'])[3].split(','):
            res[item[0]] = True
        else:
            res[item[0]] = False
    return render_template('performances.html', username=session['username'],
                           title='Спектакли', performances=performances, admin=admin,
                           in_favourites=res)


@app.route('/add_performance', methods=['GET', 'POST'])
def add_performance():
    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != ADMIN_NAME:
        return redirect('/performances')
    form = PerformanceForm()
    if form.validate_on_submit():
        title = form.title.data
        genre = form.genre.data
        time = form.time.data
        actors = form.actors.data
        description = form.description.data
        performances_model = PerformancesModel(db.get_connection())
        performances_model.insert(title, genre, time, actors, description)
        return redirect('/performances')
    return render_template('performance_form.html', title='Добавление спектакля', form=form)


@app.route('/performances/<int:performance_id>/edit', methods=['GET', 'POST'])
def edit_performance(performance_id):
    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != ADMIN_NAME:
        return redirect('/performances')
    form = PerformanceForm()
    performances_model = PerformancesModel(db.get_connection())
    if form.validate_on_submit():
        title = form.title.data
        genre = form.genre.data
        time = form.time.data
        actors = form.actors.data
        description = form.description.data
        performances_model.edit(performance_id, title, genre, time, actors, description)
        return redirect('/performances')
    exists = performances_model.exists(performance_id)
    if not exists[0]:
        return redirect('/performances')
    performance = performances_model.get(performance_id)

    form.title.process_data(performance[1])
    form.genre.process_data(performance[2])
    form.time.process_data(datetime.datetime.strptime(performance[3], '%d.%m.%Y %H:%M'))
    form.actors.process_data(performance[4])
    form.description.process_data(performance[5])

    return render_template('performance_form.html', title='Изменение данных спектакля', form=form)


@app.route('/performances/<int:performance_id>/delete')
def delete_performance(performance_id):
    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != ADMIN_NAME:
        return redirect('/performances')
    performances_model = PerformancesModel(db.get_connection())
    exists = performances_model.exists(performance_id)
    if not exists[0]:
        return redirect('/performances')
    performances_model.delete(performance_id)
    return redirect('/performances')


@app.route('/performances/<int:performance_id>')
def show_performance(performance_id):
    if 'username' not in session:
        return redirect('/login')
    performances_model = PerformancesModel(db.get_connection())
    exists = performances_model.exists(performance_id)
    if not exists[0]:
        return redirect('/performances')
    performance = performances_model.get(performance_id)
    actors_model = ActorsModel(db.get_connection())
    res_actors = []
    actors = performance[4].split(',')
    for actor in actors:
        actor = actor.strip()
        exists = actors_model.exists(actor)
        if exists[0]:
            res_actors.append(exists[1:])
    if session['username'] == ADMIN_NAME:
        admin = True
    else:
        admin = False
    users_model = UsersModel(db.get_connection())
    if str(performance_id) in users_model.get_favourites(session['user_id']).split(','):
        in_favourites = True
    else:
        in_favourites = False
    return render_template('performance.html', title=performance[1],
                           performance=performance, actors=res_actors,
                           admin=admin, in_favourites=in_favourites)


@app.route('/performances/<int:perf_id>/add')
def add_to_favourites(perf_id):
    if 'username' not in session:
        return redirect('/login')
    user_id = session['user_id']
    performances_model = PerformancesModel(db.get_connection())
    exists = performances_model.exists(perf_id)[0]
    if not exists:
        return redirect('/performances')
    users_model = UsersModel(db.get_connection())
    if str(perf_id) in users_model.get_favourites(session['user_id']).split(','):
        return redirect('/performances')
    favourites = users_model.get_favourites(user_id)
    if len(favourites) > 0:
        favourites += ',{}'.format(perf_id)
    else:
        favourites += str(perf_id)
    users_model.edit_favourites(user_id, favourites)
    return redirect('/favourites')


@app.route('/actors')
def show_actors():
    if 'username' not in session:
        return redirect('/login')
    actors_model = ActorsModel(db.get_connection())
    actors = actors_model.get_all()
    if session['username'] == ADMIN_NAME:
        admin = True
    else:
        admin = False
    return render_template('actors.html', title='Актёры', actors=actors, admin=admin)


@app.route('/add_actor', methods=['GET', 'POST'])
def add_actor():
    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != ADMIN_NAME:
        return redirect('/actors')
    form = ActorForm()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        role = form.role.data
        bio = form.bio.data
        actors_model = ActorsModel(db.get_connection())
        actors_model.insert(name, surname, role, bio)
        return redirect('/actors')
    return render_template('actor_form.html', title='Добавление актёра', form=form)


@app.route('/actors/<int:actor_id>/edit', methods=['GET', 'POST'])
def edit_actor(actor_id):
    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != ADMIN_NAME:
        return redirect('/actors')
    form = ActorForm()
    actors_model = ActorsModel(db.get_connection())
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        role = form.role.data
        bio = form.bio.data
        actors_model.edit(actor_id, name, surname, role, bio)
        return redirect('/actors')
    exists = actors_model.exists(actor_id)
    if not exists[0]:
        return redirect('/actors')
    actor = actors_model.get(actor_id)

    form.name.process_data(actor[1])
    form.surname.process_data(actor[2])
    form.role.process_data(actor[3])
    form.bio.process_data(actor[4])

    return render_template('actor_form.html', title='Редактирование профиля актёра',
                           form=form)


@app.route('/actors/<int:actor_id>/delete')
def delete_actor(actor_id):
    if 'username' not in session:
        return redirect('/login')
    elif session['username'] != ADMIN_NAME:
        return redirect('/actors')
    actors_model = ActorsModel(db.get_connection())
    actors_model.delete(actor_id)
    return redirect('/actors')


@app.route('/actors/<int:actor_id>')
def show_actor(actor_id):
    if 'username' not in session:
        return redirect('/login')
    actors_model = ActorsModel(db.get_connection())
    if not actors_model.exists(actor_id)[0]:
        return redirect('/actors')
    actor = actors_model.get(actor_id)
    if session['username'] == ADMIN_NAME:
        admin = True
    else:
        admin = False
    return render_template('actor.html', title='{} {}'.format(actor[1], actor[2]),
                           actor=actor, admin=admin)


@app.route('/favourites')
def show_favourites():
    if 'username' not in session:
        return redirect('/login')
    performances_model = PerformancesModel(db.get_connection())
    users_model = UsersModel(db.get_connection())
    res = []
    favourites = users_model.get_favourites(session['user_id'])
    for item in favourites.split(','):
        exists = performances_model.exists(item)
        if exists[0]:
            res.append(exists[1:5])
    return render_template('favourites.html', title='Избранное',
                           username=session['username'], favourites=res)


@app.route('/favourites/<int:perf_id>/delete')
def delete_from_favourites(perf_id):
    if 'username' not in session:
        return redirect('/login')
    user_id = session['user_id']
    users_model = UsersModel(db.get_connection())
    favourites = users_model.get_favourites(user_id).split(',')
    if str(perf_id) not in favourites:
        return redirect('/performances')
    del favourites[favourites.index(str(perf_id))]
    users_model.edit_favourites(user_id, ','.join(favourites))
    return redirect('/performances')


if __name__ == '__main__':
    db = DataBase()
    ActorsModel(db.get_connection()).init_table()
    PerformancesModel(db.get_connection()).init_table()
    um = UsersModel(db.get_connection())
    um.init_table()

    if not um.exists(ADMIN_NAME)[0]:
        um.insert(ADMIN_NAME, ADMIN_PASSWORD_HASH)

    app.run(port=8080, host='127.0.0.1')
