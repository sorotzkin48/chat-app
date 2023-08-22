from flask import Flask, render_template, request
import csv

app = Flask("__name__")

def add_user_to_csv(username, userpass):
    with open('users.csv', 'w') as users:
        writer = csv.writer(users)    
        writer.writerow("tt")

def check_if_user_exists(username, userpass):
    with open('users.csv', 'r') as users: 
        users_arr = csv.reader(users)
        for user in users_arr:
            if user[0] == username:
                if user[1] != userpass:
                     msg = "user with that name already exist"
                else:
                     msg = "you already registered, please login"
                return True, msg 
        return False, " "
    return False, "ERROR"

@app.route('/', methods=['GET','POST'])
def register():
    users_arr =str(csv.reader(open('users.csv', 'r')))
    for row in users_arr:
        return(row[0])
    # return render_template('register.html')
    
@app.route('/homePage', methods=['GET','POST'])
def homePage():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        user_exists, msg = check_if_user_exists(username, userpass)
        if not user_exists:
           add_user_to_csv(username, userpass)
           return "kok"
           #    ניתוב ללוגין
    return "פפפ"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
