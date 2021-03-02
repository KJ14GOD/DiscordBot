import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl


client = commands.Bot(command_prefix="^")


@client.event
async def on_ready():
  print("The bot is online")

'''@client.command(pass_context = True)
async def play(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    source = FFmpegPCMAudio('cailou.wav')
    player = voice.play(source)

  else:
    await ctx.send("You are not in voice channel")

@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("Left VC")
  else:
    await ctx.send("I am not in a voice channel. Type !play to get me in one")    
'''

@client.command()
async def play(ctx, url : str, channel):
  song_there = os.path.isfile("song.mp3")
  try:
    if song_there:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.send("Wait for music to stop playing or use stop command")
    return 

  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
  await voiceChannel.connect()
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  

  ydl_opts = {
      'format': 'bestaudio/best',
      'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
      }],
    }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      os.rename(file, "song.mp3")

  voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_connected():
        await voice.disconnect()
  else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("No audio is playing")

@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send("The audio is not paused")

@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
  await voice.stop()

client.run(os.getenv("TOKEN"))
