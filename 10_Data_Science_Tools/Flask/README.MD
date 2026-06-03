### Flask
# Flask is a lightweight web framework in Python that allows developers to create web applications and APIs with minimal code. It provides features like routing and templating, making it easy to build and scale applications.


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


# Integration of HTML in Flask: In Flask, you can return HTML content directly from your route functions as a string. When a user accesses a specific route, the corresponding function is executed, and the returned HTML string is sent back to the client's browser. The browser then renders the HTML content, allowing you to create dynamic web pages using Flask. This approach is simple and effective for small applications or when you want to quickly display some information without needing to create separate HTML files. For larger applications, you might want to use templates to manage your HTML more efficiently.