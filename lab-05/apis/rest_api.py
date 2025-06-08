import sqlite3

from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('../database/blog.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/post/simple/<int:post_id>', methods=['GET'])
def get_post_simple(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT title, author_id FROM posts WHERE id = ?', (post_id,)).fetchone()
    author = conn.execute('SELECT name FROM authors WHERE id = ?', (post['author_id'],)).fetchone()
    conn.close()
    return jsonify({
        'title': post['title'],
        'author': author['name']
    })


@app.route('/api/post/medium/<int:post_id>', methods=['GET'])
def get_post_medium(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT title, content FROM posts WHERE id = ?', (post_id,)).fetchone()
    comments = conn.execute('SELECT content FROM comments WHERE post_id = ?', (post_id,)).fetchall()
    conn.close()
    return jsonify({
        'title': post['title'],
        'content': post['content'],
        'comments': [dict(comment) for comment in comments]
    })


@app.route('/api/post/complex/<int:post_id>', methods=['GET'])
def get_post_complex(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    comments = conn.execute('''SELECT comments.content, authors.name 
                              FROM comments 
                              JOIN authors ON comments.author_id = authors.id 
                              WHERE post_id = ?''', (post_id,)).fetchall()
    author = conn.execute('SELECT name, email FROM authors WHERE id = ?', (post['author_id'],)).fetchone()
    conn.close()
    return jsonify({
        'post': dict(post),
        'author': dict(author),
        'comments': [dict(comment) for comment in comments]
    })


if __name__ == '__main__':
    app.run(port=5000)
