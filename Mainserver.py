#!C:\Users\rolan cemter\AppData\Local\Programs\Python\Python37\python.exe
from flask import Flask, request, render_template, redirect, make_response, url_for, abort
# from flask.ext.uploads import UploadSet , config
import hashlib
import MySQLdb
import listed
from difflib import get_close_matches
from werkzeug.utils import secure_filename
import os
from random import *
import string

app = Flask(__name__)

db = MySQLdb.connect('127.0.0.1', 'codeXz', 'password*', 'movies')
cursor = db.cursor()


@app.route('/')
def main():
    username = request.cookies.get('username')
    sql = 'select username from users'
    cursor.execute(sql)
    users = cursor.fetchall()
    for i in users:
        if username == i[0]:
            return render_template('main.html')

    return redirect(url_for('beforelogin'))


@app.route('/login')
def login():
    username = request.cookies.get('username')
    if not username:
        pass
    else:
        return redirect(url_for('main'))

    return render_template('login.html')


@app.route('/index', methods=['post'])
def index():
    text = request.form['email']
    passwd = request.form['pass']
    passwd = passwd + "i am so fucking sad"
    passwd = hashlib.md5(passwd.encode())
    sql = 'select * from users'
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if text == row[0]:
            if passwd.hexdigest() == row[1]:
                resp = make_response(redirect(url_for('main')))
                resp.set_cookie('username', row[0], max_age=86400)
                return resp
    return redirect(url_for('login'))


@app.route('/beforelogin')
def beforelogin():
    username = request.cookies.get('username')
    if not username:
        pass
    else:
        return redirect(url_for('main'))

    return render_template('beforelogin.html')


@app.route('/change')
def account():
    return render_template('change.html')


@app.route('/account')
def info():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('beforelogin'))
    account = request.cookies.get('username')
    sql = f'select * from users where username = "{account}"'
    try:
        cursor.execute(sql)
    except:
        db.rollback()
        return render_template('sad.html', notfound=True)
    data = cursor.fetchall()
    results = []
    if not data:
        return 'sad sad sad sad'
    for row in data:
        username = row[0]
        password = row[1]
        phone = row[2]
        profile = row[3]
        results.append(listed.de(username, password, phone))

    return render_template('info.html', username=username, phone=phone, profile=profile)


@app.route('/recover')
def recover():
    username = request.cookies.get('username')
    if not username:
        pass
    else:
        return render_template('sad.html',register=True, username=username)
    return render_template('change.html')


@app.route('/change_password', methods=['post'])
def change():
    username = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    password = password + 'i am so fucking sad'
    sql = 'select username, phonenumber from users'
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        if row[0] == username:
            if row[1] == phone:
                s = hashlib.md5(password.encode())
                d = s.hexdigest()
                sql = f'update users set password = "{d}" where username = "{username}"'
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    return render_template('sad.html', notfound=True)
                return redirect(url_for('login'))
        render_template('sad.html', notfound=True)


@app.route('/register')
def register():
    username = request.cookies.get('username')
    if not username:
        pass
    else:
        return render_template('sad.html', register=True, username=username)
    return render_template('register.html')


@app.route('/reg', methods=['post'])
def reg():
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']
    print(password)
    print(email)
    print(phone)
    try:
        profile = request.files['profile']
        print(profile)
    except:
        return 'some thing try to be happy'
    password = password + "i am so fucking sad"
    password = hashlib.md5(password.encode())
    current = os.getcwd()
    x = ''
    character = string.ascii_letters + string.digits
    while True:
        try:
            if os.path.isfile(current + '/static/profile/' + x + secure_filename(profile.filename)):
                x = "".join(choice(character) for x in range(randint(1, 2)))
            if x:
                path = '/static/profile/' + str(x) + secure_filename(profile.filename)
                profile.save(current + path)
            else:
                path = '/static/profile/' + secure_filename(profile.filename)
                profile.save(current + path)
            if True:
                break
        except:
            pass
    d = password.hexdigest()
    sql = f'insert into users (username,password, phonenumber,profile_pic) values("{email}","{d}","{phone}","{path}")'
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        return render_template('sad.html', notfound=True)
    return redirect(url_for('login'))


@app.route('/search')
def search():
    try:
        username = request.cookies.get('username')
        if not username:
            return redirect(url_for('beforelogin'))
        search = request.args.get("search")
        if search == '':
            return render_template('empty.html')
        sql = 'select name from moviename'
        cursor.execute(sql)
        names = cursor.fetchall()
        names = listed.lir(names)
        results = []
        for i in get_close_matches(search, names):
            if not i:
                return render_template('sad.html')
            try:
                sql = f'select * from moviename where name = "{i}" '
                cursor.execute(sql)
            except:
                db.rollback()
                break
            data = cursor.fetchall()
            for row in data:
                numbe = row[0]
                pathofmovie = row[1]
                pathofthumb = row[2]
                name = row[3]
                movie_ca = row[4]
                results.append(listed.de(numbe, pathofmovie, pathofthumb, name, movie_ca))
        if not results:
            return render_template('sad.html')
        return render_template('search.html', results=results)
    except:
        return render_template('sad.html', notfound=True)


@app.errorhandler(404)
def notfounded(e):
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('beforelogin'))
    return render_template('notfound.html', dde=True)


@app.route('/watch=<name>')
def watch(name):
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('beforelogin'))
    sql = f'select * from moviename where numbe = "{name}"'
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        if not data:
            return render_template('sad.html', notfound=True)
    except:
        db.rollback()
        return render_template('sad,html', notfound=True)
    data = listed.lir(data)
    return render_template('watch.html', i=data[1])


@app.route('/series=<name>')
def series(name):
    results = []
    sql = f'select movie_ca,max(season) from moviename where movie_ca = "{name}" group by movie_ca'
    cursor.execute(sql)
    data = cursor.fetchall()
    data = listed.lir(data)
    print(data)
    x = data[-1] + 1
    print(x)
    for i in range(0, x):
        sql = f'select * from moviename where movie_ca = "{name}" and season={i} limit 1'
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            numbe = row[0]
            pathmovie = row[1]
            pathofthumb = row[2]
            nae = row[3]
            movie_ca = row[4]
            season = row[5]
            episode = row[6]
            results.append(listed.series(numbe, pathmovie, pathofthumb, nae, movie_ca, season, episode))
    return render_template('MYSERIAS.html', results=results)


@app.route('/series/<name>/<season>')
def season(name, season):
    results = []
    sql = f'select * from moviename where movie_ca = "{name}" and season={season} order by episode'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    for row in data:
        numbe = row[0]
        pathmovie = row[1]
        pathofthumb = row[2]
        nae = row[3]
        movie_ca = row[4]
        season = row[5]
        epsiode = row[6]
        results.append(listed.series(numbe, pathmovie, pathofthumb, nae, movie_ca, season, epsiode))
    print(results)
    return render_template('fedede.html', results=results)


@app.route('/cat/<name>')
def catogray(name):
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('beforelogin'))
    results = []
    if name != 'series':
        sql = f'select * from moviename where movie_ca = "{name}"'
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
        except:
            db.rollback()
            return render_template('sad.html', notfound=True)
        if not data:
            return abort(404)
        for row in data:
            numbe = row[0]
            pathofmovie = row[1]
            pathofthumb = row[2]
            name = row[3]
            movie_ca = row[4]
            results.append(listed.de(numbe, pathofmovie, pathofthumb, name, movie_ca))
        return render_template('wor.html', results=results)

    else:
        sql = 'select * from cat where movie_cat != "action" and movie_cat != "comedy" and movie_cat != "cartoon" and ' \
              'movie_cat != "arabic" and movie_cat != "anime" and movie_cat != "scary" '
        cursor.execute(sql)
        serias = cursor.fetchall()
        serias = listed.lir(serias)
        for i in serias:
            sql = f'select * from moviename where movie_ca = "{i}" limit 1'
            cursor.execute(sql)
            data = cursor.fetchall()
            for row in data:
                numbe = row[0]
                pathofmovie = row[1]
                pathofthumb = row[2]
                name = row[3]
                movie_ca = row[4]
                results.append(listed.de(numbe, pathofmovie, pathofthumb, name, movie_ca))
        return render_template('wor.html', results=results, de=True)


@app.route('/upload')
def upload():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('beforelogin'))
    sql = 'select * from cat where movie_cat != "action" and movie_cat != "comedy" and movie_cat != "cartoon" and ' \
          'movie_cat != "arabic" and movie_cat != "anime" and movie_cat != "scary" '
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    data = listed.lir(data)
    return render_template('upload.html', data=data)


@app.route('/logout')
def logout():
    resp = make_response(render_template('beforelogin.html'))
    resp.set_cookie('username', expires=0)
    return resp


@app.route('/uploaded', methods=['post', 'GET'])
def uploaded():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('beforelogin'))
    if request.method == 'GET':
        return redirect(url_for('upload'))
    try:
        movie = request.files['movie']
        moviethumb = request.files['moviethumb']
        moviename = request.form['moviename']
        select = request.form.get('catog')
        print(select)
    except:
        return render_template('upload.html', wrong=True)

    # ------------------------------------------------- checking -------------------------------------------

    if not movie:
        return render_template('upload.html', missing=True, mov=True)
    if not moviethumb:
        return render_template('upload.html', missing=True, thum=True)
    test = movie.filename.split('.')
    extesion = ['avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', 'mp4', 'webm', 'ogv']
    if test[-1].lower() not in extesion:
        return render_template('upload.html', formamovie=True, de=True)
    extesion = ['jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw']
    test = moviethumb.filename.split('.')
    if test[-1].lower() not in extesion:
        return render_template('upload.html', formamovie=True, thumb=True)

    if select == 'series':
        seriasname = request.form.get('seriasname')
        season = request.form.get('season')
        epsiode = request.form.get('episode')
        print(seriasname)
        print(season)
        print(epsiode)
        if not seriasname:
            return 'please fill all parts'
        if not season:
            return 'please fill all parts'
        if not epsiode:
            return 'please fill all parts'

    # ------------------------------------------------------ saving ---------------------------------------------

    path = '/static/movies/' + secure_filename(movie.filename)
    pathofthumb = '/static/thumbs/' + secure_filename(moviethumb.filename)
    current = os.getcwd()
    print(current)
    print(path, '   ', pathofthumb)
    x = ''
    character = string.ascii_letters + string.digits
    while True:
        try:
            if os.path.isfile(current + '/static/movies/' + x + secure_filename(movie.filename)):
                x = "".join(choice(character) for x in range(randint(1, 2)))
            if x:
                path = '/static/movies/' + str(x) + secure_filename(movie.filename)
                moviethumb.save(current + path)
            else:
                path = '/static/movies/' + secure_filename(movie.filename)
                movie.save(current + '/static/movies/' + secure_filename(movie.filename))
            if True:
                break
        except:
            pass
    x = ''
    while True:
        try:
            if os.path.isfile(current + pathofthumb):
                x = ''.join(choice(character) for x in range(randint(1, 2)))
            if x:
                pathofthumb = '/static/thumbs/' + str(x) + secure_filename(moviethumb.filename)
                moviethumb.save(current + pathofthumb)
            else:
                pathofthumb = '/static/thumbs/' + secure_filename(moviethumb.filename)
                moviethumb.save(current + '/static/thumbs/' + secure_filename(moviethumb.filename))
            if True:
                break
        except:
            pass

    # ------------------------------------------------------------ inserting --------------------------

    if select == 'series':

        username = request.cookies.get('username')
        if not username:
            return redirect(url_for('beforelogin'))

        sql = f'insert into moviename(' \
            f'pathofthemovie,' \
            f'pathofthumb,' \
            f'episode_name,' \
            f'movie_ca,' \
            f'season,' \
            f'episode,' \
            f'uploaded_by) ' \
            f'values' \
            f'("{path}",' \
            f'"{pathofthumb}",' \
            f'"{secure_filename(movie.filename)}",' \
            f'"{seriasname}",' \
            f'{season},' \
            f'{epsiode},' \
            f'"{username}");'
        cursor.execute(sql)
        db.commit()

    else:
        if not moviename:
            return render_template('upload.html', missing=True, text=True)
        username = request.cookies.get('username')
        if not username:
            return redirect(url_for('beforelogin'))

        sql = f'insert into moviename (pathofthemovie,pathofthumb,name,movie_ca,uploaded_by)values("{path}","{pathofthumb}","{moviename}","{select}","{username}")'
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('i am sad')
            db.rollback()
    # sql = 'select movie_cat from cat'
    # cursor.execute(sql)
    # catogra = cursor.fetchall()
    # catogra = listed.lir(catogra)
    return render_template('uploaded.html')


@app.route('/deeded')
def sad():
    return f'''<a id="sad" href="http://127.0.0.1:5000/static/movies/EgyBest.Mr.Robot.S01E08.BluRay.1080p.x264.mp4" download > 
   
 Start automatic download!
</a>
<script>
</script>
'''


@app.route('/deeded/<name>')
def sd(name):
    s = hashlib.md5(name.encode())
    d = s.hexdigest()
    sql = f'select * from users where username = "{d}"'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return f'{d}'


# onclick="if (event.button==0)
#      setTimeout(function(){{document.body.innerHTML='thanks!'}},500)">


if __name__ == '__main__':
    app.run(port=5050,debug=True)
