from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
        'author': 'Nurdin Affandi',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Jun 17, 2025'
    },
    {
        'author': 'Joshi Boy',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Jun 18, 2025'
    }
]

@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="Flask Blog - About")

# __name__ = main when we run script with python directly
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)