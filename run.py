import os
from flask_blog import create_app, db


app = create_app()

# to run on first app run
# with app.app_context():
#     db.create_all()
#     print("✅ Database tables created!")

# __name__ = main when we run script with python directly in CLI(command-line interface)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)