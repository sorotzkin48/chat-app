from flask import Flask, render_template, request, redirect, session, flash
from enum import Enum
from datetime import datetime
import csv
import base64
import os
import re

app = Flask("__name__")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['STATIC_FOLDER'] = 'static'
app.secret_key = "my_key_here"

# Setting a new environment variable
os.environ["CURRENT_ROOM"] = ""

class user_status(Enum):
    PASS_AND_NAME_MATCH = 1
    NAME_MATCH = 2
    NO_MATCH = 3
    ERROR = 4


def encode_password(user_pass):
    """
    encodes passwords on base64
    """
    pass_bytes = user_pass.encode('ascii')
    base64_bytes = base64.b64encode(pass_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decode_password(user_pass):
    """
    decodes passwords on base64
    """
    base64_bytes = user_pass.encode('ascii')
    pass_bytes = base64.b64decode(base64_bytes)
    user_pass = pass_bytes.decode('ascii')
    return user_pass


def add_user_to_csv(username, userpass):
    """
    adds user
    """
    f = open('users.csv', 'a')
    writer = csv.writer(f)
    writer.writerow([username, encode_password(userpass)])
    f.close()


def check_input_if_valid(username, userpass):
    """
    checks input validity
    """
    if len(username) < 5:
        return False, "Name must include at least 5 character"
    if len(userpass) < 5:
        return False, "Password must include at least 5 character"  
    has_letter = any(char.isalpha() for char in userpass)
    if has_letter:
        return False, "Password must include only digits"
    return True, " "  


def check_if_user_exists(username, userpass):
    """
    checks if user exists in the program
    """
    with open('users.csv', 'r') as users: 
        users_arr = csv.reader(users)
        for user in users_arr:
            if user[0] == username:
                decoded= decode_password(user[1])
                if userpass != decoded:
                     status = 2
                else:
                     status = 1
                return status
        return 3


def remove_suffix(room):
    """
    removes suffix 
    """
    room=room[:-4]
    return room


@app.route('/', methods=['GET','POST'])
def landingPage():
    """
    redirects user who enters to register
    """
    return redirect('/register')

    
@app.route('/register', methods=['GET','POST'])
def homePage():
    """
    registers new users
    """
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        status = check_if_user_exists(username, userpass)
        if status == user_status.NO_MATCH.value:
            valid_input, msg = check_input_if_valid(username, userpass)
            if valid_input:
                add_user_to_csv(username, userpass)
                flash("User added successfully, please login")
                return redirect('/login')
            else:
                flash(msg)
                return redirect('/register')
        elif status == user_status.NAME_MATCH.value:
            flash("Name in use, please choose a diffrent name")
            return render_template("register.html")
        elif status == user_status.PASS_AND_NAME_MATCH.value:
            flash("User already exist, please login")
            return redirect("/login")
    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def loginPage():
   """
   logs users in and adds him to the current session
   """
   if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        status = check_if_user_exists(username, userpass)
        if status == user_status.PASS_AND_NAME_MATCH.value:
            flash("")
            session['username'] = username
            return redirect('/lobby')
        else: 
            flash("User not exist, please sign up")
            return redirect('/register')
   return render_template('login.html')


@app.route('/lobby', methods=['GET','POST'])
def lobbyPage():
    """
    lobby - creates new chat rooms and redirects to existing chat rooms
    """
    rooms = list(map(remove_suffix, os.listdir(os.getenv('ROOMS_DIR'))))
    if request.method == 'POST':
        new_room = request.form['new_room']
        os.environ["CURRENT_ROOM"] = new_room
        if new_room == "":
            flash("Please enter name of room")
            return render_template('lobby.html', room_names=rooms)
        if new_room in rooms: 
            flash("Room already exist")
        else:
            with open('rooms/' + os.environ["CURRENT_ROOM"] + ".txt" , 'w') as f:
                f.write("welcome \n")
                f.close()
        rooms = list(map(remove_suffix, os.listdir(os.getenv('ROOMS_DIR'))))
        render_template('lobby.html', room_names=rooms)
    return render_template('lobby.html', room_names=rooms)

@app.route('/api/clear/<room>', methods=['POST'])
def clearPage(room):
    name_to_remove= session['username']
    
    with open(f'rooms/{room}.txt', 'r') as f:
        lines = f.readlines()

    with open(f'rooms/{room}.txt', 'w') as f:
        for line in lines:
            if name_to_remove not in line:
                f.write(line)


@app.route('/health')
def healthPage():
    return "OK", 200
    

@app.route('/chat/<room>', methods=['GET','POST'])
def chatPage(room): 
    """
    renders specific chat room
    """
    return render_template('chat.html', room=room)

@app.route('/api/chat/<room>', methods=['GET', 'POST'])
def apiPage(room):
    """
    deals with messages for chat
    """
    content = " "
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
           content = f.readlines()  # קרא את כל השורות בקובץ לרשימה
           content.reverse()  # הפוך את הרשימה
           content = ''.join(content)  # פרט את הרשימה למחרוזת
    return content
            
            
@app.route('/logout', methods=['GET', 'POST'])
def logoutPage():
    """
    logs user out and removes him from the current session
    """
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.debug = True
