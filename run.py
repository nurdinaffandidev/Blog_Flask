from flask_blog import app

# __name__ = main when we run script with python directly in CLI(command-line interface)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)