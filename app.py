from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ff27c42a75864f7b443269bde9c3fef9'

posts = [
    {
        'author': 'Эзербаев Иса',
        'title': 'Python Dict',
        'content': 'First post content',
        'date_posted': 'November 4, 2020'
    },
    {
        'author': 'Эзербаев Иса',
        'title': 'Python Tuple',
        'content': 'First post content',
        'date_posted': 'November 4, 2020'
    },
]

@app.route('/')
def index():
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Аккаунт создан!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)