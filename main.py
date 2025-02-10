from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


posts = [
    {
        'id': 1,
        'title': 'Post 1',
        'content': 'This is the first post.',
        'excerpt': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
        'date_published': '05/02/2025',
        'category': 'Sports'
    },
    {
        'id': 2,
        'title': 'Second Post',
        'content': 'This is the second post.',
        'excerpt': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
        'date_published': '09/02/2025',
        'category': 'Politics'
    }
]


@app.template_filter('format_date')
def format_date(value):
    date_obj = datetime.strptime(value, '%m/%d/%Y')
    return date_obj.strftime('%B %d, %Y')


@app.route('/')
def homepage():
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post_details(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    else:
        return 'Post not found', 404

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        new_post = {
            'id': len(posts) + 1,
            'title': request.form['title'],
            'content': request.form['content'],
            'excerpt': request.form['content'][:50] + '...',
            'date_published': datetime.now().strftime('%m/%d/%Y'),
            'category': request.form['category']
        }
        posts.append(new_post)
        return redirect(url_for('homepage'))
    return render_template('add_post.html')


@app.route('/category')
def filter_by_category():
    category = request.args.get('category')
    filtered_posts = [post for post in posts if post['category'].lower() == category.lower()] if category else posts
    return render_template('index.html', posts=filtered_posts)

if __name__ == '__main__':
    app.run(debug=True)
