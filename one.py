from flask import Flask, jsonify,request, url_for, redirect, session

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '123456'

@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>h</h1>'


@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'default'})
@app.route('/home/<name>', methods = ['GET','POST'])
def home(name):
    session['name'] = name
    return '<h1>hello {}</h1> '.format(name)


@app.route('/json')
def json():
    mylist = [1,2,3,4]
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
        return '''<form method="POST" action="/theform">
                <input type="text" name="name">
                <input type="text" name="location">
                <input type="submit" name="SUbmit">
                </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
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


if __name__ == '__main__':
    app.run()