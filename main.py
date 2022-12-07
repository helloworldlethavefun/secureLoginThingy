from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        
        return render_template('login.html')
    else:
        return render_template('register.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)