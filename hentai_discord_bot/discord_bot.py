import disnake
from disnake.ext import commands
from url_parser import Parser



bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())
TOKEN = 'ur token'


@bot.event
async def on_ready():
    print('ya ready!')


@bot.command()
async def get_info(ctx):
    await ctx.send("""
        please select image source:
            1: 'hentai',
            2: 'HENTAI_GIF',
            3: 'rule34',
            4: 'HentaiSource',
            5: 'HentaiPetgirls'
        P.S: all images taken from reddit
        pls input !get_hentai (number u choose)
        
        ---------------------------------------------
        
        to clear ur urls pull - use clear_hentai_pull
        """)



@bot.command()
async def get_hentai(ctx, user_choice: str) -> None:

    parser = Parser()
    parser.store_urls(user_choice=user_choice)
    urls = parser.retrieve_urls()

    await ctx.send(f'images in pull {len(urls)}')
    for url in urls:
        await ctx.send(url)

    await ctx.send("wait for refresh images or choose another number")


@bot.command()
async def clear_hentai_pull(ctx):
    parser = Parser()
    parser.clear_urls()
    await ctx.send('all urls cleared')


if __name__ == '__main__':
    bot.run(TOKEN)
