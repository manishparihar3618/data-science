from flask import Flask
'''
It creates an instance of the Flask class, which will be our WSGI application. 
'''
app = Flask(__name__)



@app.route("/")
def welcome():
    return "<html><body><h1>Welcome to this flask course</h1></body></html>"

@app.route("/index")
def index():
    return "<html><body><h1>Welcome to the index page</h1></body></html>"

if __name__ == '__main__':
    app.run() 



