from discord.ext import commands
import json
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from asyncio import sleep
from keep_alive import keep_alive
import os
from dotenv import dotenv_values

config = dotenv_values(".env")


#returns json of all users and their song choices
def fetchUserSongs():
    with open("userSongs.json") as jsonFile:
        userSongs = json.load(jsonFile)
        jsonFile.close()
        return userSongs
    
def checkURL(url):    
    if "youtube.com" in url or "youtu.be" in url:
        return True
    return False

def updateUserSongs(user, youtubeURL):
    with open("userSongs.json", "r+") as jsonFile:
        userSongs = json.load(jsonFile)
        userSongs[user] = youtubeURL
        jsonFile.seek(0)
        jsonFile.write(json.dumps(userSongs))
        jsonFile.truncate()
        jsonFile.close()
        
def getUserSong(user):
    with open("userSongs.json") as jsonFile:
        userSongs = json.load(jsonFile)
        jsonFile.close()
        if(user in userSongs):
          return userSongs[user]
        else:
          return None

command_prefix='!'
bot = commands.Bot(command_prefix)
userSongs = fetchUserSongs()

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
    
@bot.event
async def on_voice_state_update(member, before, after):
    if(before.channel == after.channel):
        return
    
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    author = member.name
    voice_channel = after.channel
    url = getUserSong(author)
    if(url == None): return
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
    youtubeURL = ctx.message.content.replace(command_prefix+ctx.command.name,'').strip()
        
    isYoutubeLink = checkURL(youtubeURL)
    #if not youtube link, return nothing
    if(not isYoutubeLink):
        return
        
    updateUserSongs(author, youtubeURL)
    await ctx.channel.send("Added your song!")

keep_alive()
bot.run(config['TOKEN'])
