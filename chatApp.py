from flask import Flask, render_template, request, redirect, session, flash
from enum import Enum
from datetime import datetime
import csv
import base64
import os


app = Flask("__name__")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "my_key_here"


class user_status(Enum):
    PASS_AND_NAME_MATCH = 1
    NAME_MATCH = 2
    NO_MATCH = 3
    ERROR = 4


def encode_password(user_pass):
    pass_bytes = user_pass.encode('ascii')
    base64_bytes = base64.b64encode(pass_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode_password(user_pass):
    base64_bytes = user_pass.encode('ascii')
    pass_bytes = base64.b64decode(base64_bytes)
    user_pass = pass_bytes.decode('ascii')
    return user_pass

def add_user_to_csv(username, userpass):
    f = open('users.csv', 'a')
    writer = csv.writer(f)
    writer.writerow([username, encode_password(userpass)])
    f.close()

def check_if_user_exists(username, userpass):
    with open('users.csv', 'r') as users: 
        users_arr = csv.reader(users)
        for user in users_arr:
            if user[0] == username:
                decoded= decode_password(user[1])
                if userpass != decoded:
                     msg = "user name already exists"
                     status = 2
                else:
                     msg = "user exists"
                     status = 1
                return status, msg
        return 3, "user added successfully"
    return 4, "couldn't open file"

def remove_suffix(room):
    room=room[:-4]
    return room


@app.route('/', methods=['GET','POST'])
def landingPage():
    return redirect('/register')
    
@app.route('/register', methods=['GET','POST'])
def homePage():
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        status, msg = check_if_user_exists(username, userpass)
        flash(msg)
        if status == user_status.NO_MATCH.value :
            add_user_to_csv(username, userpass)
            return redirect('/login')
        elif status == user_status.NAME_MATCH.value:
           return render_template("register.html")
        elif status == user_status.PASS_AND_NAME_MATCH.value:
            return redirect("/login")
    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def loginPage():
   if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        status, msg = check_if_user_exists(username, userpass)
        flash(msg)
        if status == user_status.PASS_AND_NAME_MATCH.value:
            session['username'] = username
            return redirect('/lobby')
   return render_template('login.html')


@app.route('/lobby', methods=['GET','POST'])
def lobbyPage():
    rooms = os.listdir(os.getenv('ROOMS_DIR'))
    rooms = list(map(remove_suffix, rooms))
    if request.method == 'POST':
        new_room = request.form['new_room']
        if new_room not in rooms: 
            with open('rooms/' + new_room + ".txt" , 'w') as f:
                f.write("welcome \n")
    return render_template('lobby.html', room_names=rooms)


@app.route('/chat/<room>', methods=['GET','POST'])
def chatPage(room): 
    return render_template('chat.html', room=room)

@app.route('/api/chat/<room>', methods=['GET', 'POST'])
def apiPage(room):
    if request.method == 'POST':
        message= request.form['msg']
        name= session['username']
        time= datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with open(f'rooms/{room}.txt', 'a', newline='') as f:
            f.write(f'[{time}] {name}: {message}\n')
        f.close()
   
    if request.method == "GET":
        with open(f'rooms/{room}.txt', 'r' ) as f:
           f.seek(0)
           content = f.read()
           return content
            
            

@app.route('/logout', methods=['GET', 'POST'])
def logoutPage():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.debug = True
