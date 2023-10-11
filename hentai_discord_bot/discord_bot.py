import disnake
from disnake.ext import commands
from url_parser import Parser

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())
TOKEN = 'MTA5MzY2Mjg3NjE0MjY2NTg4MA.GDcKEG.STYf2o1V0JVGTpLRA5uPV7S-JY44AWrADhBnto'
parser = Parser()


@bot.event
async def on_ready():
    print('Bot is ready!')


@bot.command()
async def get_info(ctx):
    await ctx.send("""
        Please select an image source:
        1: 'hentai',
        2: 'HENTAI_GIF',
        3: 'rule34',
        4: 'HentaiSource',
        5: 'HentaiPetgirls'

        P.S: All images are taken from Reddit.
        Please input !get_hentai <number you choose>
        ---------------------------------------------
        To clear your URLs pool, use !clear_urls
    """)


@bot.command()
async def get_hentai(ctx, user_choice: str):
    user_id = ctx.author.id
    parser.store_urls(user_choice=user_choice, user_id=user_id)
    urls = parser.retrieve_urls(user_id)

    for url in urls:
        await ctx.send(url)


@bot.command()
async def clear_urls(ctx):
    user_id = ctx.author.id
    parser.clear_urls(user_id)
    await ctx.send('All URLs in the pool cleared')


if __name__ == '__main__':
    bot.run(TOKEN)







