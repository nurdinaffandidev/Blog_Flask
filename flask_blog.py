from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

# __name__ = main when we run script with python directly
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)