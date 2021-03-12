#!/usr/bin/python
import discord
import tmdbv3api
from tmdbv3api import TMDb
from tmdbv3api import Movie, TV
from discord.ext import commands
from discord.ext.commands.core import command, cooldown
from TOKEN import TOKEN, TMDB_TOKEN

#TMDB Setup
tmdb = TMDb()
tmdb.api_key = TMDB_TOKEN
tmdb.language = 'de'
tmdb.debug = False
movie = Movie()
tv = TV()

#Link setup
link_prefix = 'https://www.themoviedb.org/movie/'
link_suffix = '?language=de-DE'

#Command Prefix
bot = commands.Bot(command_prefix='!')

#Main setup
@bot.event
async def on_ready():
    print('Logged in and ready to go.')

#Purge Text Channel command
@bot.command()
@commands.has_permissions(administrator=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()

#Movie-Request
@bot.command()
async def mdb(ctx, *args):
    movieName = args
    movieName = ' '.join(map(str, movieName))
    print(movieName)
    if movieName.startswith('id=') == True:
        await ctx.channel.send(link_prefix + movieName.removeprefix('id=') + link_suffix)
    elif len(movieName) == 0:
        await ctx.channel.send('Nach welchen Film suchst du?\nBsp: !mdb Interstellar')
    else:
        search = movie.search(movieName)
        if len(search) == 0:
            await ctx.channel.send('Der Film', movieName, ' konnte nicht gefunden werden.')
        else:
            for res in search:
                await ctx.channel.send(link_prefix + str(res.id) + link_suffix)
                return


#---------- error handling ----------#

#Insufficient permissions to use !clean command
@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Du bist kein Admin... oder?")

bot.run(TOKEN)
