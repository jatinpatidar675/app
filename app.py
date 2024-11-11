from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, add_user, get_user, add_vote, get_results

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

init_db()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('vote'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user(username):
            flash('Username already exists')
        else:
            add_user(username, generate_password_hash(password))
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('vote'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        candidate = request.form['candidate']
        add_vote(session['user_id'], candidate)
        flash('Your vote has been recorded')
        return redirect(url_for('results'))
    return render_template('vote.html')

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    results = get_results()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)