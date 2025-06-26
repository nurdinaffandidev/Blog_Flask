from flask import Blueprint

# create instance of Blueprint
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def index():
    # setting default page
    page = request.args.get('page', 1, type=int)
    # setting number of post per page
    # Note: this results in posts becoming a Pagination object
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title="Flask Blog - About")