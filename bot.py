import discord
from environs import Env
from mcpi import minecraft
import mcpi.block as block

env = Env()
env.read_env(".env", recurse=False)
token = env("TOKEN")
server = env("SERVER", "localhost")
port = env.int("PORT", 4711)
bot = discord.Client()
mc = minecraft.Minecraft.create(server, port)

# https://www.raspberrypi-spy.co.uk/2014/09/raspberry-pi-minecraft-block-id-number-reference/
blocos = {
    "ar": block.AIR.id,
    "pedra": block.STONE.id,
    "grama": block.GRASS.id,
    "terra": block.DIRT.id,
    "água": block.WATER.id,
    "lava": block.LAVA.id,
    "areia": block.SAND.id,
    "madeira": block.WOOD.id,
    "vidro": block.GLASS.id,
    "cama": block.BED.id,
    "lã": block.WOOL.id,
    "tnt": block.TNT.id,
    "ferro": block.IRON_BLOCK.id,
    "ouro": block.GOLD_BLOCK.id,
    "fogo": block.FIRE.id,
    "gelo": block.ICE.id
}


async def react(message, reaction):
    if reaction == 'thumb up':
        await message.add_reaction('\U0001F44D')
    elif reaction == 'thumb down':
        await message.add_reaction('\U0001F44E')
    else:
        await message.add_reaction('\U000026CF')


@bot.event
async def on_ready():
    print('Conectado!')
    game = discord.Game("Jogando Minecraft Pi...")
    await bot.change_presence(activity=game)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('comandos'):
        await react(message, 'thumb up')
        await message.channel.send(
            'Comandos:\n'
            + '- onde: onde estou?\n'
            + '- tipos: tipos de blocos para construir.\n'
            + '- teleportar X Y Z: teleportar o jogador para as coordenadas.\n'
            + '- bloco X Y Z BLOCO: criar um BLOCO na coordenada.\n'
            + '- blocos X1 Y1 Z1 X2 Y2 Z2 BLOCO: criar vários blocos dentro das coordenadas.'
        )

    if message.content.startswith('onde'):
        await react(message, 'pick')
        x, y, z = mc.player.getTilePos()
        msg = str(x) + ', ' + str(y) + ', ' + str(z)
        mc.postToChat(msg)

    if message.content.startswith('tipos'):
        await react(message, 'thumb up')
        await message.channel.send(
            'Os tipos de blocos são: '
            + ', '.join(blocos.keys())
        )

    if message.content.startswith('teleportar'):
        msg = message.content.split(' ')
        try:
            x0 = float(msg[1])
            y0 = float(msg[2])
            z0 = float(msg[3])
            await react(message, 'pick')
            mc.player.setPos(x0, y0, z0)
        except:
            await react(message, 'thumb down')

    if message.content.startswith('bloco'):
        # Executar o comando no Minecraft Pi...
        msg = message.content.split(' ')
        try:
            x0 = float(msg[1])
            y0 = float(msg[2])
            z0 = float(msg[3])
            if msg[0] == 'bloco':
                bloco = blocos[msg[4]]
                await react(message, 'pick')
                mc.setBlock(x0, y0, z0, bloco)
            else:
                x1 = float(msg[4])
                y1 = float(msg[5])
                z1 = float(msg[6])
                bloco = blocos[msg[7]]
                await react(message, 'pick')
                mc.setBlocks(x0, y0, z0, x1, y1, z1, bloco)
        except:
            await react(message, 'thumb down')

bot.run(token)
