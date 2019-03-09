from flask import Flask, render_template, url_for, request, session, redirect, abort
from flask_pymongo import PyMongo, pymongo
import bcrypt
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mangastuff'
app.config['MONGO_URI'] = 'mongodb://user:2252010baby@ds159785-a0.mlab.com:59785,ds159785-a1.mlab.com:59785/mangastuff?replicaSet=rs-ds159785'
app.config['SECRET_KEY'] = '0f9dc56d2288afa6e10b8d97577fe25b'


mongo = PyMongo(app)



# home/index route
@app.route('/')
def home():
    front_page_manga = list(mongo.db.update_spider.find())
    popular_manga_list = []

    for item in front_page_manga[0]['popular_manga']:
        popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

    # sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
    # for item in sample_list:
    #     popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))

    latest_mange_releases = []
    sample_list_latest = ['troll_trap', 'little_13','jy918373','df918543','deatte_5_byou_de_battle','yotsukoto','martial_art_successor','the_ghostly_doctor','yd918542','oa917623','the_descendant_of_the_dynasty','uat947546','crossing_the_boundary_twins','hw917776','kishibe_no_uta','antinomy','takeda_shingen_yokoyama_mitsuteru','when_night_falls','legend_of_immortals','bw918450']
    for item in sample_list_latest:
        latest_mange_releases.append(mongo.db.all_manga_details.find_one({'id':item}))


    most_popular_manga = []
    sample_list_most = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550']
    for item in sample_list_most:
        most_popular_manga.append(mongo.db.all_manga_details.find_one({'id':item}))

    genres_categories = list(mongo.db.genres_categories.find())
    genres = genres_categories[0]['genres']
    categories = genres_categories[0]['categories']

    # with open('test.html', 'w+') as outfile:
    #     json.dump(most_popular_manga, outfile)

    return render_template('index.html', mangas = front_page_manga, popular_manga_list=popular_manga_list, latest_mange_releases=latest_mange_releases, most_popular_manga=most_popular_manga, genres=genres, categories=categories)





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
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            # if  bcrypt.check_password_hash(login_user['password'], request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('account'))
            error_message = 'Invalid username or password, Please try again!'
            return render_template('login.html', error_message = error_message)

    return render_template('login.html')







@app.route('/home_json_tooltips/')
def home_json_tooltips():
    return render_template('home_json_tooltips.html')


# Main manga page with pagintion. Used in all types of manga page
@app.route('/manga/')
def manga():
    items = mongo.db.all_manga_details

    #Getting total manga number
    total_manga = len(list(items.find()))

    #getting total page number
    offset = 24
    page_number = total_manga / offset
    if total_manga % offset == 0:
        total_page_number = int(str(page_number).split('.')[0])
    else:
        total_page_number = int(str(page_number).split('.')[0]) + 1

    #pagination code
    first_prev_page = 0
    second_prev_page = 0
    current_page = 0
    first_next_page = 0
    second_next_page = 0


    if int(request.args['page']) == 1:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = 0
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == 2:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == total_page_number - 1:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = 0
    elif int(request.args['page']) == total_page_number:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = 0
        second_next_page = 0
    elif int(request.args['page']) > 3:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    else:
        first_prev_page = 1
        second_prev_page = 2
        current_page = 3
        first_next_page = 4
        second_next_page = 5
    #pagination code ends here

    page_offset = (current_page-1) * 24
    limit = 24

    starting_manga_id = items.find().sort('_id', pymongo.ASCENDING)
    last_manga_id = starting_manga_id[page_offset]['_id']

    # all_manga = list(items.find().limit(offset))
    all_manga = list(items.find({'_id':{'$gte':last_manga_id}}).sort('_id', pymongo.ASCENDING).limit(limit))

    front_page_manga = list(mongo.db.update_spider.find())
    popular_manga_list = []

    # for item in front_page_manga[0]['popular_manga']:
    #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

    sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
    for item in sample_list:
        popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


    genres_categories = list(mongo.db.genres_categories.find())
    genres = genres_categories[0]['genres']
    categories = genres_categories[0]['categories']


    return render_template('manga.html', all_manga=all_manga, total_manga = total_manga, total_page_number = total_page_number, current_page = current_page, first_prev_page = first_prev_page, second_prev_page = second_prev_page, first_next_page = first_next_page, second_next_page = second_next_page, popular_manga_list=popular_manga_list, genres=genres, categories=categories)





@app.route('/manga-hot/')
def manga_hot():
    items = mongo.db.all_manga_details

    #Getting total manga number
    total_manga = len(list(items.find()))

    #getting total page number
    offset = 24
    page_number = total_manga / offset
    if total_manga % offset == 0:
        total_page_number = int(str(page_number).split('.')[0])
    else:
        total_page_number = int(str(page_number).split('.')[0]) + 1

    #pagination code
    first_prev_page = 0
    second_prev_page = 0
    current_page = 0
    first_next_page = 0
    second_next_page = 0


    if int(request.args['page']) == 1:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = 0
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == 2:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == total_page_number - 1:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = 0
    elif int(request.args['page']) == total_page_number:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = 0
        second_next_page = 0
    elif int(request.args['page']) > 3:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    else:
        first_prev_page = 1
        second_prev_page = 2
        current_page = 3
        first_next_page = 4
        second_next_page = 5
    #pagination code ends here

    page_offset = (current_page-1) * 24
    limit = 24

    starting_manga_id = items.find().sort('votes', pymongo.DESCENDING)
    last_manga_id = starting_manga_id[page_offset]['_id']

    # all_manga = list(items.find().limit(offset))
    all_manga = list(items.find({'_id':{'$gte':last_manga_id}}).sort('votes', pymongo.DESCENDING).limit(limit))

    front_page_manga = list(mongo.db.update_spider.find())
    popular_manga_list = []

    # for item in front_page_manga[0]['popular_manga']:
    #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

    sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
    for item in sample_list:
        popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


    genres_categories = list(mongo.db.genres_categories.find())
    genres = genres_categories[0]['genres']
    categories = genres_categories[0]['categories']


    return render_template('manga-hot.html', all_manga=all_manga, total_manga = total_manga, total_page_number = total_page_number, current_page = current_page, first_prev_page = first_prev_page, second_prev_page = second_prev_page, first_next_page = first_next_page, second_next_page = second_next_page, popular_manga_list=popular_manga_list, genres=genres, categories=categories)






@app.route('/manga-new/')
def manga_new():
    items = mongo.db.all_manga_details

    #Getting total manga number
    total_manga = len(list(items.find()))

    #getting total page number
    offset = 24
    page_number = total_manga / offset
    if total_manga % offset == 0:
        total_page_number = int(str(page_number).split('.')[0])
    else:
        total_page_number = int(str(page_number).split('.')[0]) + 1

    #pagination code
    first_prev_page = 0
    second_prev_page = 0
    current_page = 0
    first_next_page = 0
    second_next_page = 0


    if int(request.args['page']) == 1:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = 0
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == 2:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == total_page_number - 1:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = 0
    elif int(request.args['page']) == total_page_number:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = 0
        second_next_page = 0
    elif int(request.args['page']) > 3:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    else:
        first_prev_page = 1
        second_prev_page = 2
        current_page = 3
        first_next_page = 4
        second_next_page = 5
    #pagination code ends here

    page_offset = (current_page-1) * 24
    limit = 24

    starting_manga_id = items.find().sort('votes', pymongo.ASCENDING)
    last_manga_id = starting_manga_id[page_offset]['_id']

    # all_manga = list(items.find().limit(offset))
    all_manga = list(items.find({'_id':{'$gte':last_manga_id}}).sort('votes', pymongo.ASCENDING).limit(limit))

    front_page_manga = list(mongo.db.update_spider.find())
    popular_manga_list = []

    # for item in front_page_manga[0]['popular_manga']:
    #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

    sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
    for item in sample_list:
        popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


    genres_categories = list(mongo.db.genres_categories.find())
    genres = genres_categories[0]['genres']
    categories = genres_categories[0]['categories']


    return render_template('manga-new.html', all_manga=all_manga, total_manga = total_manga, total_page_number = total_page_number, current_page = current_page, first_prev_page = first_prev_page, second_prev_page = second_prev_page, first_next_page = first_next_page, second_next_page = second_next_page, popular_manga_list=popular_manga_list, genres=genres, categories=categories)






@app.route('/manga-completed/')
def manga_completed():
    items = mongo.db.all_manga_details

    #Getting total manga number
    total_manga = len(list(items.find()))

    #getting total page number
    offset = 24
    page_number = total_manga / offset
    if total_manga % offset == 0:
        total_page_number = int(str(page_number).split('.')[0])
    else:
        total_page_number = int(str(page_number).split('.')[0]) + 1

    #pagination code
    first_prev_page = 0
    second_prev_page = 0
    current_page = 0
    first_next_page = 0
    second_next_page = 0


    if int(request.args['page']) == 1:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = 0
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == 2:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == total_page_number - 1:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = 0
    elif int(request.args['page']) == total_page_number:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = 0
        second_next_page = 0
    elif int(request.args['page']) > 3:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    else:
        first_prev_page = 1
        second_prev_page = 2
        current_page = 3
        first_next_page = 4
        second_next_page = 5
    #pagination code ends here

    page_offset = (current_page-1) * 24
    limit = 24

    starting_manga_id = items.find().sort('status', pymongo.ASCENDING)
    last_manga_id = starting_manga_id[page_offset]['_id']

    # all_manga = list(items.find().limit(offset))
    all_manga = list(items.find({'_id':{'$gte':last_manga_id}}).sort('status', pymongo.ASCENDING).limit(limit))

    front_page_manga = list(mongo.db.update_spider.find())
    popular_manga_list = []

    # for item in front_page_manga[0]['popular_manga']:
    #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

    sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
    for item in sample_list:
        popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


    genres_categories = list(mongo.db.genres_categories.find())
    genres = genres_categories[0]['genres']
    categories = genres_categories[0]['categories']


    return render_template('manga-completed.html', all_manga=all_manga, total_manga = total_manga, total_page_number = total_page_number, current_page = current_page, first_prev_page = first_prev_page, second_prev_page = second_prev_page, first_next_page = first_next_page, second_next_page = second_next_page, popular_manga_list=popular_manga_list, genres=genres, categories=categories)






@app.route('/manga-genre-search/')
def manga_genre_search():
    items = mongo.db.all_manga_details

    #Getting total manga number
    total_manga = len(list(items.find()))

    #getting total page number
    offset = 24
    page_number = total_manga / offset
    if total_manga % offset == 0:
        total_page_number = int(str(page_number).split('.')[0])
    else:
        total_page_number = int(str(page_number).split('.')[0]) + 1

    #pagination code
    first_prev_page = 0
    second_prev_page = 0
    current_page = 0
    first_next_page = 0
    second_next_page = 0


    if int(request.args['page']) == 1:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = 0
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == 2:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == total_page_number - 1:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = 0
    elif int(request.args['page']) == total_page_number:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = 0
        second_next_page = 0
    elif int(request.args['page']) > 3:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    else:
        first_prev_page = 1
        second_prev_page = 2
        current_page = 3
        first_next_page = 4
        second_next_page = 5
    #pagination code ends here

    page_offset = (current_page-1) * 24
    limit = 24

    starting_manga_id = items.find().sort('status', pymongo.ASCENDING)
    last_manga_id = starting_manga_id[page_offset]['_id']

    # all_manga = list(items.find().limit(offset))
    all_manga = list(items.find({'_id':{'$gte':last_manga_id}}).sort('status', pymongo.ASCENDING).limit(limit))

    front_page_manga = list(mongo.db.update_spider.find())
    popular_manga_list = []

    # for item in front_page_manga[0]['popular_manga']:
    #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

    sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
    for item in sample_list:
        popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


    genres_categories = list(mongo.db.genres_categories.find())
    genres = genres_categories[0]['genres']
    categories = genres_categories[0]['categories']


    return render_template('manga-genre-search.html', all_manga=all_manga, total_manga = total_manga, total_page_number = total_page_number, current_page = current_page, first_prev_page = first_prev_page, second_prev_page = second_prev_page, first_next_page = first_next_page, second_next_page = second_next_page, popular_manga_list=popular_manga_list, genres=genres, categories=categories)







@app.route('/manga-id/<string:manga_id>')
def manga_id(manga_id):
    # manga_id = request.url.split('/')[-1]
    manga_id = manga_id
    manga_details = mongo.db.all_manga_details.find_one({'id':manga_id})
    manga_chapter_list = mongo.db.manga_chapter_list.find_one({'manga_id':manga_id})

    manga_id_here = manga_chapter_list['manga_id']
    iteration = len(manga_chapter_list['chapter_id'])
    chapter_list = []
    for x in range(iteration):
        chapter_list.append([manga_chapter_list['chapter_id'][x]])

    for x in range(iteration):
        chapter_list[x].append(manga_chapter_list['full_chapter_url'][x])

    for x in range(iteration):
        chapter_list[x].append(manga_chapter_list['chapter_link_text'][x])

    for x in range(iteration):
        chapter_list[x].append(manga_chapter_list['chapter_time_uploaded'][x])

    #store the manga id in users document for history page
    if session:
        user_name = session['username']
        users = mongo.db.users
        history_data = users.find_one({'name':user_name})

        if 'history' not in history_data:
            users.update_one({'name': user_name}, {'$push': {'history':''}})

        history_data_again = users.find_one({'name':user_name})
        if manga_id not in history_data_again['history']:
            users.update_one({'name': user_name}, {'$push': {'history': manga_id}})


    front_page_manga = list(mongo.db.update_spider.find())
    popular_manga_list = []

    # for item in front_page_manga[0]['popular_manga']:
    #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

    sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
    for item in sample_list:
        popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


    most_popular_manga = []
    sample_list_most = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550']
    for item in sample_list_most:
        most_popular_manga.append(mongo.db.all_manga_details.find_one({'id':item}))

    genres_categories = list(mongo.db.genres_categories.find())
    genres = genres_categories[0]['genres']
    categories = genres_categories[0]['categories']

    return render_template('manga-id.html', manga_details = manga_details, chapter_list = chapter_list, manga_id_here = manga_id_here, popular_manga_list=popular_manga_list, most_popular_manga=most_popular_manga, genres=genres, categories=categories)



@app.route('/manga-id-chapter/<string:manga_id>/<string:chapter_id>')
def manga_id_chapter(manga_id, chapter_id):
    manga_id =manga_id
    chapter_id = chapter_id
    url = request.url
    manga_details = mongo.db.all_manga_details.find_one({'id':manga_id})
    manga_chapter_list = mongo.db.manga_chapter_list.find_one({'manga_id':manga_id})
    chapter_list = list(mongo.db.manga_each_chapter_image_list_with_manga_id.find({'manga_id':manga_id}))

    index = manga_chapter_list['chapter_id'].index(chapter_id)
    image_list = chapter_list[index]['manga_each_chapter_image_list_with_manga_id']
    current_chapter_text = manga_chapter_list['chapter_link_text'][index]

    current_chapter_id = chapter_id
    if index == len(manga_chapter_list['chapter_id'])-1:
        prev_chapter_id = manga_chapter_list['chapter_id'][1 + 1]
    else:
        prev_chapter_id = manga_chapter_list['chapter_id'][index + 1]
    next_chapter_id = manga_chapter_list['chapter_id'][index - 1]
    next_chapter_identifier = True
    prev_chapter_id_identifier = True

    if current_chapter_id == manga_chapter_list['chapter_id'][0]:
        next_chapter_identifier = False

    if current_chapter_id == manga_chapter_list['chapter_id'][-1]:
        prev_chapter_id_identifier = False

    iteration_number = len(manga_chapter_list['chapter_id'])
    chapter_option_list = []
    for y in range(iteration_number):
        chapter_option_list.append([manga_chapter_list['chapter_id'][y]])
    for y in range(iteration_number):
        chapter_option_list[y].append(manga_chapter_list['chapter_link_text'][y])

    related_manga = mongo.db.all_manga_details.find().sort('last_updated', pymongo.ASCENDING).limit(12)

    return render_template('manga-id-chapter.html', manga_details = manga_details, manga_chapter_list = manga_chapter_list, image_list = image_list, url = url, current_chapter_id = current_chapter_text, prev_chapter_id = prev_chapter_id, next_chapter_id = next_chapter_id, next_chapter_identifier=next_chapter_identifier, prev_chapter_id_identifier=prev_chapter_id_identifier, chapter_option_list=chapter_option_list, related_manga=related_manga)





# This is test route to see data structure in template. This route isn't used in website template
@app.route('/data/')
def data():
    # item = mongo.db.items
    # getty = item.find_one({"data_id": "9m40"})
    # return getty['title']
    total_page_number = 29
    first_prev_page = 0
    second_prev_page = 0
    current_page = 0
    first_next_page = 0
    second_next_page = 0


    if int(request.args['page']) == 1:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = 0
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == 2:
        current_page = int(request.args['page'])
        first_prev_page = 0
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    elif int(request.args['page']) == total_page_number - 1:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = 0
    elif int(request.args['page']) == total_page_number:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = 0
        second_next_page = 0
    elif int(request.args['page']) > 3:
        current_page = int(request.args['page'])
        first_prev_page = current_page - 2
        second_prev_page = current_page - 1
        first_next_page = current_page + 1
        second_next_page = current_page + 2
    else:
        first_prev_page = 1
        second_prev_page = 2
        current_page = 3
        first_next_page = 4
        second_next_page = 5



    items = mongo.db.all_manga_details
    all_items = list(items.find().limit(10))

    return render_template('data.html', all_items=all_items, current_page = current_page, first_prev_page = first_prev_page, second_prev_page = second_prev_page, first_next_page = first_next_page, second_next_page = second_next_page)


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
        front_page_manga = list(mongo.db.update_spider.find())
        popular_manga_list = []

        # for item in front_page_manga[0]['popular_manga']:
        #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))

        sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
        for item in sample_list:
            popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


        most_popular_manga = []
        sample_list_most = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550']
        for item in sample_list_most:
            most_popular_manga.append(mongo.db.all_manga_details.find_one({'id':item}))

        genres_categories = list(mongo.db.genres_categories.find())
        genres = genres_categories[0]['genres']
        categories = genres_categories[0]['categories']


        user_name = session['username']
        users = mongo.db.users
        bookmark_id = users.find_one({'name':user_name})
        # history = {'history':manga_id}
        # users.update({ "name":username },{$set : {"history":manga_id}})
        # users.insert_one(history)
        bookmark_data = []
        total_bookmark = 0
        if 'bookmark' in bookmark_id:
            total_bookmark = len(bookmark_id['bookmark'])
            for bookmark_manga in bookmark_id['bookmark']:
                bookmark_data.append(mongo.db.all_manga_details.find_one({'id':bookmark_manga}))



        return render_template('bookmark.html', popular_manga_list=popular_manga_list, most_popular_manga=most_popular_manga, genres=genres, categories=categories, bookmark_data=bookmark_data, total_bookmark=total_bookmark)
    else:
        return redirect(url_for('login'))








# history route
@app.route('/history/')
def history():
    if session:
        popular_manga_list = []
        # for item in front_page_manga[0]['popular_manga']:
        #     popular_manga_list.append(list(mongo.db.all_manga_details.find_one({'id':item})))
        sample_list = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550', 'gp918549', 'mata_kataomou', 'jc917903']
        for item in sample_list:
            popular_manga_list.append(mongo.db.all_manga_details.find_one({'id':item}))


        most_popular_manga = []
        sample_list_most = ['kz918552', 'radiant', 'zi918554', 'saikyou_no_shuzoku_ga_ningen_datta_ken', 'le918553', 'xy918428', 'zw918006', 'jb918548', 'gk918551', 'gg918550']
        for item in sample_list_most:
            most_popular_manga.append(mongo.db.all_manga_details.find_one({'id':item}))

        genres_categories = list(mongo.db.genres_categories.find())
        genres = genres_categories[0]['genres']
        categories = genres_categories[0]['categories']


        user_name = session['username']
        users = mongo.db.users
        history_id = users.find_one({'name':user_name})
        # history = {'history':manga_id}
        # users.update({ "name":username },{$set : {"history":manga_id}})
        # users.insert_one(history)
        history_data = []
        for history_manga in history_id['history']:
            history_data.append(mongo.db.all_manga_details.find_one({'id':history_manga}))


        return render_template('history.html', most_popular_manga=most_popular_manga, genres=genres, categories=categories, popular_manga_list=popular_manga_list, history_data=history_data)
    else:
        return redirect(url_for('login'))




# add bookmark route
@app.route('/add-bookmark/<string:manga_id>')
def add_bookmark(manga_id):


    if session:
        manga_id = request.url.split('/')[-1]
        #store the manga id in users document for history page
        user_name = session['username']
        users = mongo.db.users
        bookmark_data = users.find_one({'name':user_name})

        if 'bookmark' not in bookmark_data:
            users.update_one({'name': user_name}, {'$push': {'bookmark':''}})

        bookmark_data_again = users.find_one({'name':user_name})
        if manga_id not in bookmark_data['bookmark']:
            users.update_one({'name': user_name}, {'$push': {'bookmark': manga_id}})

        return redirect(url_for('bookmark'))
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
    app.run(debug=True)
