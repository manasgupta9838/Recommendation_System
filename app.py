import pandas as pd
import subprocess
import email
from classifier import Recommendation
from flask import Flask, render_template, url_for, redirect, request, session
from flask.json import jsonify
import database

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)
app = Flask(__name__)
app.secret_key = "Manas123#*"


# dataset = tablib.Dataset()
# with open(os.path.join(os.path.dirname(__file__),'email.csv')) as f:
#     dataset.csv = f.read()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    errors = ''
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        if username and password:
            db = database.Database()
            userlist = db.get_user()
            for row in userlist:
                if username in row and password in row:
                    session['id'] = row[0]
                    session['username'] = row[1]
                    message = "successful logged in"
                    return redirect(url_for('show_content1', data=message))
            errors = "invalid crediential"
        else:
            errors = "please fii details"
    return render_template('login.html', errors=errors)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    errors = ""
    if request.method == 'POST':
        db = database.Database()
        try:
            db.create_user_table()
        except:
            pass
        username = request.form.get('user')
        email = request.form.get('email')
        password = request.form.get('pwd')
        cpassword = request.form.get('cpwd')

        if password == cpassword and len(username) > 2 and len(
                password) > 6 and '@' in email and '.com' in email and len(email) > 11:
            signup = db.add_user(username, email, password)
            return render_template("index.html", data="success")
        else:
            errors = 'invalid details'
    return render_template('signup.html', errors=errors)


@app.route('/user_preferences', methods=['GET', 'POST'])
def user_preferences():
    errors = ""
    if request.method == 'POST':
        db = database.Database()
        ans1 = request.form.get('price')
        ans2 = request.form.get('brand')
        ans3 = request.form.get('brands')
        ans4 = request.form.get('rating')
        ans5 = request.form.get('review')
        db.create_choice_table()
        id = session.get('id')
        db.add_option(id, 'price', ans1)
        db.add_option(id, 'brand', ans2)
        db.add_option(id, 'brands', ans3)
        db.add_option(id, 'rating', ans4)
        db.add_option(id, 'review', ans5)
        return redirect(url_for('show_content1'))

    return render_template('user_preferences.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/showcontent')
def show_content1():
    return render_template('show_content.html')


@app.route('/fetch_request_fast')
def fetch_request_fast():
    search_item = request.args.get('content')
    csv_file = f'data/products_{search_item}_details.csv'
    try:
        df = pd.read_csv(csv_file)
        htmltable = df.to_html()
        return jsonify({'success': "done", 'datatable': htmltable, 'file': csv_file})
    except subprocess.CalledProcessError as e:
        print(e)
        return jsonify({'error': str(e)})


@app.route('/fetch_request')
def fetch_request():
    search_item = request.args.get('content')
    path_for_link = f'data/product_{search_item}_link.csv'
    csv_file = f'data/products_{search_item}_details.csv'
    command = f"scrapy runspider scrapers/link_scraper.py -o {path_for_link} -a search={search_item}"
    command2 = f"scrapy runspider scrapers/product_scraper.py -o {csv_file} -a path={path_for_link}"
    try:
        with open('scraper.log', 'w') as f:
            request_status = subprocess.call(command.split(), stdout=f)
            request_status2 = subprocess.call(command2.split(), stdout=f)
        df = pd.read_csv(csv_file)
        htmltable = df.to_html()
        return jsonify({'success': "done", 'datatable': htmltable, 'file': csv_file})
    except subprocess.CalledProcessError as e:
        print(e)
        return jsonify({'error': str(e)})


@app.route('/recommend')
def recommend():
    filename = request.args.get('file')
    rcmd = Recommendation(filename, session.get('id'))
    rcmd.clean_df()
    prices = rcmd.recommend_by_price()
    ratings = rcmd.recommend_by_rating()
    review = rcmd.recommend_by_review()
    brands = rcmd.recommend_by_brand()
    product1 = prices[['title', 'link']]
    product2 = ratings[['title', 'link']]
    product3 = review[['title', 'link']]
    try:
        if brands.size > 0:
            product4 = brands[['title', 'link']]
            return render_template('recommend.html', p=product1, rt=product2, rv=product3, bd=product4)
        return render_template('recommend.html', p=product1, rt=product2, rv=product3)
    except Exception as e:
        return render_template('recommend.html', p=product1, rt=product2, rv=product3)


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
