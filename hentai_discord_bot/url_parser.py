import requests
import sqlite3


class Parser:
    def __init__(self):
        pass

    urls = {
        '1': 'hentai',
        '2': 'HENTAI_GIF',
        '3': 'rule34',
        '4': 'HentaiSource',
        '5': 'HentaiPetgirls'
    }

    def store_urls(self, user_choice: str, user_id: int) -> None:
        headers = {'User-Agent': 'UUFyJFQzUZtOrqEPXD5opJ-R6RZEkw'}

        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    url TEXT
                )
            ''')
            conn.commit()

            subreddit_name = self.urls[user_choice]
            url = f'https://www.reddit.com/r/{subreddit_name}/new.json'

            req = requests.get(url, headers=headers)

            data = req.json()
            for post in data['data']['children']:
                if 'url' in post['data']:
                    url_to_insert = post['data']['url']

                    cursor.execute('SELECT id FROM posts WHERE url = ? AND user_id = ?', (url_to_insert, user_id))
                    existing_url = cursor.fetchone()

                    if existing_url is None:
                        cursor.execute('INSERT INTO posts (user_id, url) VALUES (?, ?)', (user_id, url_to_insert))
                        conn.commit()

    @staticmethod
    def retrieve_urls(user_id: int) -> list:
        urls = []
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT url FROM posts WHERE user_id = ?', (user_id,))
            rows = cursor.fetchall()
            urls.extend([row[0] for row in rows])

        return urls

    @staticmethod
    def clear_urls(user_id):
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()

            cursor.execute('DELETE FROM posts WHERE user_id = ?', (user_id,))
            conn.commit()


