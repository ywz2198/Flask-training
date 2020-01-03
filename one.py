from flask import Flask, jsonify,request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '123456'

#数据库
def connect_db(): 
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#关闭数据库
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#页面
@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>h</h1>'


@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'default'})
@app.route('/home/<name>', methods = ['GET','POST'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()

    return render_template('home.html',name = name, display=False, \
         mylist = [1,2,3,4],dic = [{'name': 'zack'},{'name': 'zoe'}], results=results)
    # return '<h1>hello {}</h1> '.format(name)


@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'Notinsession'
    return jsonify({'key' : 'value', 'list' : [1,2,333], 'name' : name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return 'query page{},{}'.format(name,location)

@app.route('/theform', methods=['GET','POST'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        # return  'hello{}, {},submitted'.format(name, location)
        return redirect(url_for('home', name=name,location=location))


@app.route('/theform', methods=['POST'])
def process():
    name = request.form['name']
    location= request.form['location']
    return 'Hello ,{},from {}'.format(name, location)

@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    return jsonify({'result' : 'success', 'name' : name ,'location' : location, 'randomkeyinlist' : randomlist[1]})

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select * from users')
    results = cur.fetchall()
    return '<h1>The ID is {}, name{}, location{}</h1>'.format(results[1]['id'], results[1]['name'], results[1]['location'])

if __name__ == '__main__':
    app.run()