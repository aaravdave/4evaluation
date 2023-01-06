import pymongo
from flask import *
from passlib.hash import sha256_crypt

app = Flask("To-do List")
app.secret_key = '4evaluation'
client = pymongo.MongoClient('mongodb+srv://livequipdata:xupdiw-wojro5-jEhbyw@cluster0.oirex.mongodb.net/?retryWrites=true&w=majority', tls=True, tlsAllowInvalidCertificates=True)
db = client.contactmanager


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'logged' in session and session['logged']:
            return render_template('index.html', tasks=list(db.tasks.find({'username': session['logged']})))
        else:
            flash('You must sign in to view notes.')
            return redirect('/login')
    if request.method == 'POST':
        if 'add' in request.form and request.form['text'] and not db.tasks.find_one({'username': session['logged'], 'text': request.form['text']}):
            db.tasks.insert_one({'username': session['logged'], 'text': request.form['text'], 'complete': False})
        if 'delete' in request.form:
            db.tasks.delete_one({'username': session['logged'], 'text': request.form['task']})
        if 'okay' in request.form:
            db.tasks.update_one({'username': session['logged'], 'text': request.form['old']}, {'$set': {'username': session['logged'], 'text': request.form['new'], 'complete': db.tasks.find_one({'username': session['logged'], 'text': request.form['old']})['complete']}})
        if 'complete' in request.form:
            db.tasks.update_one({'username': session['logged'], 'text': request.form['task']}, {'$set': {'username': session['logged'], 'text': request.form['task'], 'complete': not db.tasks.find_one({'username': session['logged'], 'text': request.form['task']})['complete']}})
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = db.contacts.find_one({'username': request.form['username']})
        if not username:
            flash('Username not found.')
            return redirect('/login')
        elif not sha256_crypt.verify(request.form['password'], username['password']):
            print(username, '2')
            flash('Password incorrect.')
            return redirect('/login')
        else:
            session['logged'] = request.form['username']
            flash('Successfully signed in.')
            return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        if db.contacts.find_one({'username': request.form['username']}):
            flash('Username taken.')
            return redirect('/signup')
        elif request.form['password'] != request.form['confirm']:
            flash('Passwords do not match.')
            return redirect('/signup')
        else:
            db.contacts.insert_one({'username': request.form['username'], 'password': sha256_crypt.hash(request.form['password'])})
            flash('Successfully signed up.')
            return redirect('/login')


@app.route('/logout')
def logout():
    session['logged'] = False
    flash('Successfully signed out.')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
