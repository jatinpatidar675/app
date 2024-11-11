import sqlite3

def init_db():
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS votes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER UNIQUE NOT NULL,
                  candidate TEXT NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return {'id': user[0], 'username': user[1], 'password': user[2]}
    return None

def add_vote(user_id, candidate):
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO votes (user_id, candidate) VALUES (?, ?)", (user_id, candidate))
    conn.commit()
    conn.close()

def get_results():
    conn = sqlite3.connect('voting.db')
    c = conn.cursor()
    c.execute("SELECT candidate, COUNT(*) FROM votes GROUP BY candidate")
    results = c.fetchall()
    conn.close()
    return results