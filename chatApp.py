from flask import Flask, render_template, request, redirect
import csv
from enum import Enum
import base64

class user_status(Enum):
    PASS_AND_NAME_MATCH = 1
    NAME_MATCH = 2
    NO_MATCH = 3
    ERROR = 4


app = Flask("__name__")

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
    writer.writerow([username,userpass])
    f.close()

def check_if_user_exists(username, userpass):
    with open('users.csv', 'r') as users: 
        users_arr = csv.reader(users)
        for user in users_arr:
            if user[0] == username:
                if user[1] != userpass:
                     msg = "user with that name already exist"
                     status = 1
                else:
                     msg = "you already registered, please login"
                     status = 2
                return status, msg
        return 3, " "
    return 4, "ERROR"

    
@app.route('/', methods=['GET','POST'])
def homePage():
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        status, msg = check_if_user_exists(username, userpass)
        if status == user_status.NO_MATCH.value :
            add_user_to_csv(username, userpass)
            return redirect('/login')
        elif status == user_status.NAME_MATCH.value:
           return render_template("login.html")
    return render_template("register.html")
@app.route('/login', methods=['GET','POST'])
def loginPage():
   if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        user_exists, msg = check_if_user_exists(username, userpass)
        if user_exists:
            return render_template('login.html')
   return render_template('login.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.debug = True