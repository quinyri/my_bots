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


    def store_urls(self, user_choice: str):

        headers = {'User-Agent': 'UUFyJFQzUZtOrqEPXD5opJ-R6RZEkw'}

        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
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

                    cursor.execute('SELECT id FROM posts WHERE url = ?', (url_to_insert,))
                    existing_url = cursor.fetchone()

                    if existing_url is None:
                        cursor.execute('INSERT INTO posts (url) VALUES (?)', (url_to_insert,))
                        conn.commit()


    def retrieve_urls(self):
        urls = []
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT url FROM posts')
            rows = cursor.fetchall()
            for row in rows:
                urls.append(row[0])
        return urls

    @staticmethod
    def clear_urls():
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()

            cursor.execute('DELETE FROM posts')
            conn.commit()







