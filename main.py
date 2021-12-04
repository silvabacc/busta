from discord.ext import commands
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from asyncio import sleep
from keep_alive import keep_alive
from replit import db

from dotenv import dotenv_values

config = dotenv_values(".env")

def checkURL(url):
    if "youtube.com" in url or "youtu.be" in url:
        return True
    return False

command_prefix = '!'
bot = commands.Bot(command_prefix)

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

@bot.event
async def on_voice_state_update(member, before, after):
    user_enabled = db[member.name + "_preferences"]

    if not user_enabled:
        return

    if (before.channel == after.channel):
        return

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    author = member.name
    voice_channel = after.channel
    url = db[author]
    if (url == None): return
    vc = await voice_channel.connect()

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            vc.play(FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS))
            vc.is_playing()
            await sleep(30)
            await vc.disconnect()


@bot.command()
async def setsong(ctx):
    author = ctx.author.name
    youtubeURL = ctx.message.content.replace(command_prefix + ctx.command.name, '').strip()

    isYoutubeLink = checkURL(youtubeURL)
    # if not youtube link, return nothing
    if (not isYoutubeLink):
        return

    db[author] = youtubeURL
    await ctx.channel.send("Added your song!")

@bot.command()
async def toggle(ctx):
    db[ctx.author.name + "_preferences"] = not db[ctx.author.name + "_preferences"]

    if db[ctx.author.name + "_preferences"]:
        await ctx.channel.send('Your intro song is now enabled')
    else:
        await ctx.channel.send('Your intro song is now disabled')

keep_alive()
bot.run(config['TOKEN'])