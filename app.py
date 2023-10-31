from bottle import Bottle, request, run, template
import sqlite3

app = Bottle()

def create_table():
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_table()




@app.route('/')
def index():
    return "Welcome to the User Registration System"



@app.route('/register', method='GET')
def registration_form():
    return template('registration_form')



@app.route('/register', method='POST')
def register_user():
    username = request.forms.get('username')
    password = request.forms.get('password')

    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return "Registration successful for user: {}".format(username)




@app.route('/login', method='GET')
def login_form():
    return template('login_form')




@app.route('/login', method='POST')
def login_user():
    username = request.forms.get('username')
    password = request.forms.get('password')

    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[1] == password:
        return "Login successful for user: {}".format(username)
    else:
        return "Invalid login credentials"

if __name__ == '__main__':
    run(app, host='localhost', port=8080)
