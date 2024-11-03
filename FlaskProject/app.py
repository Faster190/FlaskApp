from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, logout_user, login_user, current_user
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gdbase.db'
app.config['SECRET_KEY'] = 'fdfsdfsdfsdfsd08sadas8'
db = SQLAlchemy(app)
app.app_context().push()
manager = LoginManager(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Users %r>' % self.id

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    intro = db.Column(db.String(200))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer())


    def __repr__(self):
        return '<Games %r>' % self.id


@app.route('/')
def main_page():
    cur_user = current_user
    posts = Posts.query.order_by(Posts.date.desc()).all()
    return render_template("main_page.html", posts=posts, user=cur_user, profile=False)

@app.route('/<int:id>')
def post_page(id):
    cur_user = current_user
    post = Posts.query.get(id)
    author = Users.query.get(post.user_id)
    return render_template("post_page.html", post=post, user=cur_user, author=author)

@app.route('/<int:id>/delete')
def post_delete(id):
    cur_user = current_user
    if not cur_user.is_anonymous:
        post = Posts.query.get_or_404(id)
        author = Users.query.get(post.user_id)
        if author.username == cur_user.username:
            try:
                db.session.delete(post)
                db.session.commit()
                return redirect('/')
            except:
                error = 'При удалении статьи произошла ошибка.'
                return render_template("error.html", error=error, user=cur_user)
    return redirect('/login')

@app.route('/<int:id>/update', methods=['POST', 'GET'])
def update_post(id):
    cur_user = current_user
    if not cur_user.is_anonymous:
        post = Posts.query.get(id)
        author = Users.query.get(post.user_id)
        if author.username == cur_user.username:
            if request.method == 'POST':
                post.title = request.form['title']
                post.intro = request.form['intro']
                post.text = request.form['text']

                try:
                    db.session.commit()
                    return redirect('/')
                except:
                    error = 'При редактировании статьи произошла ошибка. Попробуйте позже.'
                    return render_template("error.html", error = error, user=cur_user)
            else:
                return render_template("update_post.html", post=post, user=cur_user)

    return redirect('/login')

@app.route('/create-post', methods=['POST', 'GET'])
def create_post():
    cur_user = current_user
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        post = Posts(title=title, intro=intro, text=text, user_id=cur_user.id)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            error = 'При добавлении статьи произошла ошибка. Попробуйте позже.'
            return render_template("error.html", error = error, user=cur_user)
    else:
        return render_template("create_post.html", user=cur_user)

@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    cur_user = current_user
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']

        err = False
        user = Users.query.filter_by(username=username).first()
        if user:
            flash("Пользователь с таким именем уже существует")
            err = True
        user = Users.query.filter_by(email=email).first()
        if user:
            flash("Пользователь с такой почтой уже существует")
            err = True
        if len(username) > 30 or len(username) < 3:
            flash("Имя пользователя должно быть от 3 до 30 символов")
            err = True
        if password1 != password2:
            flash("Пароли должны совпадать")
            err = True
        if len(password1) > 20 or len(password1) < 8:
            flash("Пароль должен быть от 8 до 20 символов")
            err = True
        if err:
            return render_template("registration.html", user=cur_user)

        hush = generate_password_hash(password1)
        user = Users(username=username, password=hush, email=email)
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/')
        except:
            error = 'При регистрации пользователя произошла ошибка. Попробуйте позже.'
            return render_template("error.html", error = error, user=cur_user)
    else:
        return render_template("registration.html", user=cur_user)

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    cur_user = current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
            else:
                flash("Неверный пароль")
                return render_template("login.html", user=cur_user)
        else:
            flash("Нет пользователя с таким именем")
            return render_template("login.html", user=cur_user)
        return redirect('/')
    else:
        return render_template("login.html", user=cur_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route(f'/profile')
def profile():
    cur_user = current_user
    if not cur_user.is_anonymous:
        posts = Posts.query.filter(Posts.user_id == cur_user.id).all()
        return render_template("main_page.html", posts=posts, user=cur_user, profile=True)
    return redirect('/login')

@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

if __name__ == "__main__":
    app.run(debug=True)