from flask import Flask
'''
It creates an instance of the Flask class, which will be our WSGI application. 
'''
app = Flask(__name__)



@app.route("/")
def welcome():
    return "Welcome to this flask course"

if __name__ == '__main__':
    app.run() 


















