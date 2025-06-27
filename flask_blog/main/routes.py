from flask import render_template, request, Blueprint
from flask_blog.models import Post


# create instance of Blueprint
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def index():
    """
       Render the home page with paginated blog posts.

       - Retrieves the current page number from query parameters (defaults to 1).
       - Fetches posts ordered by most recent first.
       - Paginates the posts (5 per page).

       Returns:
           Response: Rendered home page with paginated posts.
   """
    # setting default page
    page = request.args.get('page', 1, type=int)
    # setting number of post per page
    # Note: this results in posts becoming a Pagination object
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    """
        Render the About page.

        Returns:
            Response: Rendered static about page with title context.
    """
    return render_template('about.html', title="Flask Blog - About")