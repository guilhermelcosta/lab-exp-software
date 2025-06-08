import sqlite3

def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS authors (
                 id INTEGER PRIMARY KEY,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                 id INTEGER PRIMARY KEY,
                 title TEXT NOT NULL,
                 content TEXT NOT NULL,
                 author_id INTEGER,
                 FOREIGN KEY(author_id) REFERENCES authors(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS comments (
                 id INTEGER PRIMARY KEY,
                 post_id INTEGER,
                 author_id INTEGER,
                 content TEXT NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(post_id) REFERENCES posts(id),
                 FOREIGN KEY(author_id) REFERENCES authors(id))''')

    # Dados de exemplo
    authors = [
        (1, 'Ana Silva', 'ana@exemplo.com'),
        (2, 'Carlos Oliveira', 'carlos@exemplo.com')
    ]

    posts = [
        (1, 'Introdução ao REST', 'Conteúdo sobre REST...', 1),
        (2, 'GraphQL Básico', 'Conteúdo sobre GraphQL...', 2)
    ]

    comments = [
        (1, 1, 2, 'Ótimo post!', '2023-06-01 10:00:00'),
        (2, 1, 1, 'Obrigada!', '2023-06-01 11:30:00'),
        (3, 2, 1, 'Muito útil', '2023-06-02 09:15:00')
    ]

    c.executemany('INSERT INTO authors VALUES (?,?,?)', authors)
    c.executemany('INSERT INTO posts VALUES (?,?,?,?)', posts)
    c.executemany('INSERT INTO comments VALUES (?,?,?,?,?)', comments)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()