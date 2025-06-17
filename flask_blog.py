from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return "<h1>Home Page</h1>"

@app.route("/about")
def about():
    return "<h1>Home Page</h1>"

# __name__ = main when we run script with python directly
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)