from app import app, db
from flask import request, render_template, flash, redirect, url_for
from models import User, Universe
from forms import SignUpForm, LoginForm, NewUniverse
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash('No user found with these credentials!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
    return render_template('login.html', title='Log In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Success!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up',
                           form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NewUniverse()
    if request.method == 'POST' and form.validate():
        new_universe = Universe(name=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(new_universe)
        db.session.commit()
    unis = Universe.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', title='Dashboard', universes=unis, form=form)


@app.route('/write')
def write():
    return render_template('editor.html', title='Write')

@app.route('/settings')
def settings():
    return render_template('home.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
