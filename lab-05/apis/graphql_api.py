import sqlite3

import graphene
from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, Field, Int, String, List


class AuthorType(ObjectType):
    id = Int()
    name = String()
    email = String()


class CommentType(ObjectType):
    id = Int()
    content = String()
    author = Field(AuthorType)
    timestamp = String()


class PostType(ObjectType):
    id = Int()
    title = String()
    content = String()
    author = Field(AuthorType)
    comments = List(CommentType)


class Query(ObjectType):
    post_simple = Field(PostType, post_id=Int(required=True))
    post_medium = Field(PostType, post_id=Int(required=True))
    post_complex = Field(PostType, post_id=Int(required=True))

    def resolve_post_simple(self, info, post_id):
        return fetch_post_data(post_id, ['title', 'author.name'])

    def resolve_post_medium(self, info, post_id):
        return fetch_post_data(post_id, ['title', 'content', 'comments.content'])

    def resolve_post_complex(self, info, post_id):
        return fetch_post_data(post_id, ['id', 'title', 'content',
                                         'author.id', 'author.name', 'author.email',
                                         'comments.id', 'comments.content',
                                         'comments.author.name', 'comments.timestamp'])


def fetch_post_data(post_id, fields):
    conn = sqlite3.connect('../database/blog.db')
    conn.row_factory = sqlite3.Row

    post_fields = []
    if 'id' in fields: post_fields.append('id')
    if 'title' in fields: post_fields.append('title')
    if 'content' in fields: post_fields.append('content')
    if 'author_id' in fields or any(f.startswith('author.') for f in fields): post_fields.append('author_id')
    post_query = f"SELECT {', '.join(post_fields)} FROM posts WHERE id = ?"

    post = conn.execute(post_query, (post_id,)).fetchone()
    if not post:
        return None

    author = None
    if any(f.startswith('author.') for f in fields):
        author = conn.execute('SELECT id, name, email FROM authors WHERE id = ?', (post['author_id'],)).fetchone()

    comments = []
    if any(f.startswith('comments.') for f in fields):
        comments = conn.execute('''SELECT comments.*, authors.name 
                                   FROM comments 
                                   JOIN authors ON comments.author_id = authors.id 
                                   WHERE post_id = ?''', (post_id,)).fetchall()

    conn.close()

    return {
        'id': post['id'] if 'id' in fields else None,
        'title': post['title'] if 'title' in fields else None,
        'content': post['content'] if 'content' in fields else None,
        'author': {
            'id': author['id'] if 'author.id' in fields else None,
            'name': author['name'] if 'author.name' in fields else None,
            'email': author['email'] if 'author.email' in fields else None
        } if any(f.startswith('author.') for f in fields) else None,
        'comments': [
            {
                'id': c['id'] if 'comments.id' in fields else None,
                'content': c['content'] if 'comments.content' in fields else None,
                'author': {'name': c['name']} if 'comments.author.name' in fields else None,
                'timestamp': str(c['timestamp']) if 'comments.timestamp' in fields else None
            } for c in comments
        ] if any(f.startswith('comments.') for f in fields) else []
    }


schema = graphene.Schema(query=Query)
app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(port=5001)
