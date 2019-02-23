from flask import Flask, render_template, url_for, request, session, redirect, abort
from flask_pymongo import PyMongo, pymongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'nineanimes'
app.config['MONGO_URI'] = 'mongodb://aqurds:2252010baby@ds115436.mlab.com:15436/nineanimes'

mongo = PyMongo(app)




@app.route('/')
def home():
    items = mongo.db.items
    all_items = items.find().sort('views', pymongo.DESCENDING).limit(56)
    return render_template("index.html", all_items = all_items)


@app.route('/home_json_tooltips/')
def home_json_tooltips():
    return render_template('home_json_tooltips.html')


@app.route('/manga/')
def manga():
    return render_template('manga.html')


@app.route('/manga-id/')
def manga_id():
    return render_template('manga-id.html')


@app.route('/manga-id-chapter/')
def manga_id_chapter():
    return render_template('manga-id-chapter.html')


# Register route
@app.route('/register/', methods=['POST', 'GET'])
def register():
    if session:
        return redirect(url_for('account'))
    if request.method == 'POST':
        users = mongo.db.users
        current_user = users.find_one({'name' : request.form['username']})

        if current_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass, 'displayname' : request.form['displayname'], 'email' : request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('account'))
        error_message = 'Username already exist, please choose different one!'
        return render_template('register.html', error_message = error_message)
    return render_template('register.html')



# Login route
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if session:
        return redirect(url_for('account'))
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            # if  bcrypt.check_password_hash(login_user['password'], request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('account'))
            error_message = 'Invalid username or password, Please try again!'
            return render_template('login.html', error_message = error_message)

    return render_template('login.html')




# This is test route to see data structure in template. This route isn't used in website template
@app.route('/data/')
def data():
    # item = mongo.db.items
    # getty = item.find_one({"data_id": "9m40"})
    # return getty['title']

    items = mongo.db.items
    all_items = items.find()

    return render_template('data.html', all_items=all_items)


@app.route('/account/')
def account():
    if session:
        return render_template('account.html')
    else:
        return redirect(url_for('login'))


# Logout route
@app.route('/logout/')
def logout():
    if session:
        session.clear()
        return redirect(url_for('logout'))
    else:
        return redirect(url_for('home'))


@app.route('/update/')
def update():
    if session:
        return render_template('update.html')
    else:
        return redirect(url_for('login'))



@app.route('/password-change/')
def password_change():
    if session:
        return render_template('password-change.html')
    else:
        return redirect(url_for('login'))


# bookmark route
@app.route('/bookmark/')
def bookmark():
    if session:
        return render_template('bookmark.html')
    else:
        return redirect(url_for('login'))


# history route
@app.route('/history/')
def history():
    if session:
        return render_template('history.html')
    else:
        return redirect(url_for('login'))


@app.route('/test/')
def test():
    data = {'username':'aqurds', 'job':'coder'}
    user = mongo.db.testdata
    user.insert(data)
    return 'data added'


if __name__ == '__main__':
    app.secret_key = '0f9dc56d2288afa6e10b8d97577fe25b'
    app.run(debug=True)
