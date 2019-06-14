from environs import Env
import discord

env = Env()
env.read_env()
token = env("TOKEN")
bot = discord.Client()


@bot.event
async def on_ready():
    print('Conectado!')
    game = discord.Game("Jogando Minecraft Pi...")
    await bot.change_presence(activity=game)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('bloco'):
        # Executar o comando no Minecraft Pi...
        await message.add_reaction('\U000026cf')


bot.run(token)
