import disnake
from disnake.ext import commands
from bot_backend import Bot
from disnake.ui import Button, View

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())
backend = Bot('identifier.sqlite')


@bot.command()
async def start(ctx):
    user_id = ctx.author.id

    view = View()
    load_button = Button(style=disnake.ButtonStyle.gray, label='Load')
    next_button = Button(style=disnake.ButtonStyle.blurple, label="Start")
    favorite_button = Button(style=disnake.ButtonStyle.red, label='Favorite Images')

    view.add_item(load_button)
    view.add_item(next_button)
    view.add_item(favorite_button)

    async def load_button_callback(interaction):
        await interaction.response.send_message(content="Images loaded!")
        backend.reg_all_urls(interaction.user.id)

    async def next_button_callback(interaction):
        user_id3 = interaction.user.id
        new_url = backend.get_one_url(user_id3)
        if new_url:
            backend.del_one_url(user_id3, url=new_url[0])
            new_embed = disnake.Embed(color=disnake.Color.purple())
            new_url = backend.get_one_url(user_id3)
            if new_url:
                new_embed.set_image(url=new_url[0])
            else:
                new_embed.add_field(name="No More Images", value="There are no more images to display.")
            await interaction.response.send_message(embed=new_embed, view=view1)
        else:
            await interaction.response.send_message(content="No More Images")

    async def favorite_button_callback(interaction):
        user_id1 = interaction.user.id
        new_url = backend.get_fav_url(user_id1)
        if new_url:
            new_embed = disnake.Embed(color=disnake.Color.red())
            new_embed.set_image(url=new_url[0])
            await interaction.response.send_message(embed=new_embed, view=view2)
        else:
            await interaction.response.send_message(content="No Favorite Images")

    load_button.callback = load_button_callback
    next_button.callback = next_button_callback
    favorite_button.callback = favorite_button_callback

    menu_embed = disnake.Embed(color=disnake.Color.purple(), description='Menu')
    menu_embed.add_field(name='Most Important', value='If the buttons do not respond, use !start.')
    menu_embed.add_field(name='Load', value='Loads images for display (important for viewing programs).')
    menu_embed.add_field(name='Next', value='After loading, you can click this button to start viewing. '
                         'Under the image, there will be a <Menu> button that will return you here. '
                         'The <Save> button saves the selected image, and the <Next> button shows the next message.')
    menu_embed.add_field(name='Favorite Images', value='After clicking this button, you can view your saved images ('
                                                       'if any).')
    menu_embed.set_image(url='https://i.pinimg.com/236x/e8/e9/ec/e8e9ec2ca3ed1493332b246ffabdcdfb.jpg')

    view1 = View()
    save_button1 = Button(style=disnake.ButtonStyle.green, label="Save")
    stop_button1 = Button(style=disnake.ButtonStyle.red, label="Menu")
    next_button1 = Button(style=disnake.ButtonStyle.blurple, label="Next")

    view1.add_item(stop_button1)
    view1.add_item(save_button1)
    view1.add_item(next_button1)

    async def save_callback(interaction):
        user_id1 = interaction.user.id
        url2 = backend.get_one_url(user_id)[0]
        backend.reg_fav_url(user_id1, url2)
        await interaction.response.send_message(content="Image saved!")

    async def menu_callback(interaction):
        await interaction.response.send_message(embed=menu_embed, view=view)

    async def next_callback(interaction):
        user_id1 = interaction.user.id
        new_url = backend.get_one_url(user_id1)
        if new_url:
            backend.del_one_url(user_id1, url=new_url[0])
            new_embed = disnake.Embed(color=disnake.Color.purple())
            new_url = backend.get_one_url(user_id1)
            if new_url:
                new_embed.set_image(url=new_url[0])
            await interaction.response.send_message(embed=new_embed, view=view1)
        else:
            await interaction.response.send_message(content="No More Images")

    save_button1.callback = save_callback
    stop_button1.callback = menu_callback
    next_button1.callback = next_callback

    view2 = View()
    menu_button2 = Button(style=disnake.ButtonStyle.green, label='Menu')
    delete_button2 = Button(style=disnake.ButtonStyle.red, label='Delete')
    next_button2 = Button(style=disnake.ButtonStyle.blurple, label='Next')

    view2.add_item(menu_button2)
    view2.add_item(delete_button2)
    view2.add_item(next_button2)

    async def menu_button_callback(interaction):
        await interaction.response.send_message(embed=menu_embed, view=view)

    async def delete_button_callback(interaction):
        user_id1 = interaction.user.id
        url = backend.get_fav_url(user_id1)[0]
        backend.del_fav_url(user_id1, url)
        await interaction.response.send_message(content="Image deleted!")

    async def next_fav_button_callback(interaction):
        user_id1 = interaction.user.id
        new_url = backend.get_fav_url(user_id1)
        if new_url:
            backend.del_fav_url(user_id1, new_url[0])
            backend.reg_fav_url(user_id1, new_url[0])
            new_url = backend.get_fav_url(user_id1)
            new_embed = disnake.Embed(color=disnake.Color.red())
            new_embed.set_image(url=new_url[0])
            await interaction.response.send_message(embed=new_embed, view=view2)
        else:
            await interaction.response.send_message(content="No Favorite Images")

    menu_button2.callback = menu_button_callback
    delete_button2.callback = delete_button_callback
    next_button2.callback = next_fav_button_callback

    await ctx.send(embed=menu_embed, view=view)

try:
    bot.run('')
except Exception as e:
    print(e)
