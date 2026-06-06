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

## Explain above content:The code above is a simple Flask application that defines two routes: the root route ("/") and the "/index" route. When a user accesses the root route, they will see a welcome message displayed in an HTML format. Similarly, when they access the "/index" route, they will see a different welcome message. The application is run using the `app.run()` method, which starts the Flask development server.

## Integration of HTML in Flask: In Flask, you can return HTML content directly from your route functions as a string. When a user accesses a specific route, the corresponding function is executed, and the returned HTML string is sent back to the client's browser. The browser then renders the HTML content, allowing you to create dynamic web pages using Flask. This approach is simple and effective for small applications or when you want to quickly display some information without needing to create separate HTML files. For larger applications, you might want to use templates to manage your HTML more efficiently.