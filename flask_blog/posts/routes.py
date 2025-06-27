from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm


# create instance of Blueprint
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
        Create a new blog post.

        - Displays a form to the logged-in user.
        - On valid submission, saves the post to the database.
        - Redirects to the homepage after creation.

        Returns:
            Response: Renders form or redirects after successful submission.
    """
    form = PostForm()
    if form.validate_on_submit():
        # creating post and adding post to db
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')  # flash: to send a one-time alert
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    """
        Display a single blog post.

        Args:
            post_id (int): ID of the post to display.

        Returns:
            Response: Renders the post detail template.
    """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
        Update an existing blog post.

        - Only the author can update their own post.
        - Pre-fills the form with existing data.
        - Saves updated content to the database.

        Args:
            post_id (int): ID of the post to update.

        Returns:
            Response: Renders form or redirects after successful update.

        Raises:
            404 Resource Not Found: If post does not exist.
            403 Forbidden: If the user is not the author.
    """
    # get post if exist else throw 404 error
    post = Post.query.get_or_404(post_id)
    # check authorized user for post else throw 403 error
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        # update post and commit to db
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id)) # redirect required due to post-get-redirect pattern
    elif request.method == 'GET':
        # populate form with existing post title and content
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
       Delete an existing blog post.

       - Only the post's author is authorized to delete it.
       - Post is removed from the database.

       Args:
           post_id (int): ID of the post to delete.

       Returns:
           Response: Redirects to the homepage after deletion.

       Raises:
           404 Resource Not Found: If post does not exist.
           403 Forbidden: If the user is not the author.
   """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))
