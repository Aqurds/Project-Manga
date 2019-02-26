from flask import Flask, render_template, url_for, request, session, redirect, abort
from flask_pymongo import PyMongo, pymongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'aqurds'
app.config['MONGO_URI'] = 'mongodb://user:2252010baby@ds249035.mlab.com:49035/aqurds'

mongo = PyMongo(app)




@app.route('/')
def home():
    # items = mongo.db.items
    # all_items = items.find().sort('views', pymongo.DESCENDING).limit(56)
    # return render_template("index.html", all_items = all_items)
    return render_template('index.html')


@app.route('/home_json_tooltips/')
def home_json_tooltips():
    return render_template('home_json_tooltips.html')


@app.route('/manga/')
def manga():
    items = mongo.db.all_manga_details
    all_manga = list(items.find().limit(24))

    total_manga = len(list(mongo.db.all_manga_details.find()))
    # number = []
    # for item in total_manga:
    #     number.append(item)
    return render_template('manga.html', all_manga=all_manga, total_manga = total_manga)


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

    items = mongo.db.all_manga_details
    all_items = list(items.find().limit(10))

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


# bookmark route: check if the session exist, if exist collect the user name and store the manga id. Fetch the manga id from user table and show the manga details.
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

# history route will be critical as we need to memorize the total visited page by the userself. so in manga route each time a manga is loaded, we need to check the session, if session exist, then collect the user name and manga id the user visiting. Store the manga id in the user column with and fetch the history data and show in the history page. That's all.


#run the scrapy on 15 min schedule and collect the manga id from front page which are updated in the last 15 min, then update only those manga with specific login

if __name__ == '__main__':
    app.secret_key = '0f9dc56d2288afa6e10b8d97577fe25b'
    app.run(debug=True)
