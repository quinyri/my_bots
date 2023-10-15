from sqlf import SQLiteDatabase, UserRepository
import requests


class Bot:
    def __init__(self, name):
        db = SQLiteDatabase(name)
        user_repository = UserRepository(db)
        self.user_repository = user_repository

        self.urls = {
            '1': 'hentai',
            '2': 'HENTAI_GIF',
            '3': 'rule34',
            '4': 'HentaiSource',
            '5': 'HentaiPetgirls'
        }

        self.headers = {'User-Agent': 'UUFyJFQzUZtOrqEPXD5opJ-R6RZEkw'}

    def parse_urls(self) -> list:
        user_urls = []
        for key, subreddit in self.urls.items():
            req_url = f'https://www.reddit.com/r/{subreddit}/new.json'
            req = requests.get(req_url, headers=self.headers)

            data = req.json()
            for post in data['data']['children']:
                if 'url' in post['data']:
                    url_to_insert = post['data']['url']
                    user_urls.append(url_to_insert)

        return user_urls

    def reg_user(self, user_id: int):
        self.user_repository.input_user_id(user_id)

    def del_fav_url(self, user_id: int, url: str):
        self.user_repository.delete_fav_url(user_id, url)

    def reg_fav_url(self, user_id: int, url: str):
        self.user_repository.input_fav_urls(user_id, url)

    def reg_all_urls(self, user_id: int):
        user_urls = self.parse_urls()
        self.user_repository.input_all_urls(user_id, user_urls)

    def get_one_url(self, user_id: int):
        return self.user_repository.get_one_url(user_id)

    def get_fav_url(self, user_id: int):
        return self.user_repository.get_fav_url(user_id)

    def del_one_url(self, user_id: int, url: str):
        self.user_repository.delete_one_url(user_id, url)

    def get_all_urls(self, user_id: int):
        return self.user_repository.get_all_urls(user_id)


if __name__ == '__main__':
    bot = Bot('identifier.sqlite')
    url = bot.get_all_urls(632978996593950720)
    print(url[2][0])




