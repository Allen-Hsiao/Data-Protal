from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory, jsonify
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random, secure value.

# Load usernames and hashed passwords from an Excel file
user_data = pd.read_excel(r"C:\Users\allen\Desktop\VS_Code\Enerlites_data_portal\user_data.xlsx")
base_directory = r"I:\Files Portal"


def get_user_directory(username):
    tech_users = ["RayHe", "Sunny-Tech", "Bill", "PaulT", "Debby", "Jerimiah", "Evelyn", "PaulY", 
                "Nani", "Keilani-Tech", "Arielle", "Jake", "Gordon", "Nicole", "Connie", "Anita", "Thai", "Jorge", "Sharon", "Angel-Tech"]
    
    marketing_users = ["Keilani-Market", "Sunny-Market", "Binbin", "Angel-Market"]

    acconting_users = ["Amy", "Angel-ACC"]

    tech_users_HJ = ["Tinkle"]
    
    if username in tech_users:
        return os.path.join(base_directory, "Tech Dept-MTLC")
    elif username in marketing_users:
        return os.path.join(base_directory, "Marketing Dept")
    elif username in acconting_users:
        return os.path.join(base_directory, "Accounting Dept")
    elif username in tech_users_HJ:
        return os.path.join(base_directory, "Tech Dept-HJ")
    else:
        # Default directory for unknown users
        return base_directory


@app.route('/')
def home():
    # if 'username' in session:
    #     return f'Logged in as {session["username"]} | <a href="/logout">Logout</a>'
    # return 'You are not logged in | <a href="/login">Login</a>'
    return redirect(url_for('login'))

@app.route('/index')
def index():
    print("Program executing: Enerlites Data Portal")
    username = session['username']
    file_directory = get_user_directory(username)
    folder_list = get_folders(file_directory)
    return render_template('index.html', folders=folder_list)

@app.route('/download/<folder>/<filename>')
def download_files(folder, filename):
    username = session['username']
    file_directory = get_user_directory(username)
    folder_path = os.path.join(file_directory, folder)

    return send_from_directory(folder_path, filename, as_attachment=True)

def get_folders(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

@app.route('/get_files/<folder>')
def get_files(folder):
    username = session['username']
    file_directory = get_user_directory(username)
    folder_path = os.path.join(file_directory, folder)  # Adjust the path accordingly
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    return jsonify({'files': files})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global username
        username = request.form['username']
        password = request.form['password']
        
        # Check if the entered username exists and the password is correct
        user_entry = user_data[user_data['username'] == username]
        if not user_entry.empty and password == str(user_entry.iloc[0]['password']):
            session['username'] = username
            print("Login:", username)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    # print("Logout:", username)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)