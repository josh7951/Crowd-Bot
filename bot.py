import os
from discord import channel
import requests
import discord 
import random 

from dotenv import load_dotenv, find_dotenv
from discord.ext import commands

load_dotenv(find_dotenv())

client = commands.Bot(command_prefix = '?')
client.remove_command('help')

@client.event 
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with depression | ?help'))
    print('Bot is ready.')    

@client.command()
async def help(ctx):
    ##author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    embed.set_author(name='Command List')
    embed.add_field(name="crowd <query>", value="Displays live crowd data after taking query input and approximate location input (be as close to accurate with the address as possible :))", inline=False)
    embed.add_field(name="magicman <question>", value="Magic 8Ball\nalso can use `?8ball`", inline=False)
    embed.add_field(name="ping", value="Used to test latency", inline=False)

    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong - latency: {round(client.latency)*1000} ms')

@client.command(aliases = ['8ball', 'magicman'])
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes.", 
                 "Ask again later.", 
                 "Better not tell you now.", 
                 "Cannot predict now.", 
                 "Concentrate and ask again.",
                 "Don’t count on it.", 
                 "It is certain.", 
                 "It is decidedly so.", 
                 "Most likely.", 
                 "My reply is no.", 
                 "My sources say no.",
                 "Outlook not so good.", 
                 "Outlook good.", 
                 "Reply hazy, try again.", 
                 "Signs point to yes.", 
                 "Very doubtful.", 
                 "Without a doubt.",
                 "Yes.", 
                 "Yes – definitely.", 
                 "You may rely on it."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def test(ctx):
    url = f"https://besttime.app/api/v1/keys/{os.getenv('BT_PRIVATE_KEY')}"
    response = requests.request("GET", url)
    await ctx.send(response.json())

@client.command()
async def crowd(ctx, *, query):
    await ctx.send(f'Enter the approximate address of {query}:')

    user_input = await client.wait_for('message', check=lambda m: m.channel == ctx.channel)
    query_location = user_input.content

    url = "https://besttime.app/api/v1/forecasts/live"

    params = {
        'api_key_private': {os.getenv('BT_PRIVATE_KEY')},
        'venue_name': {query},
        'venue_address': {query_location}
    }

    response = requests.request("POST", url, params=params)
    await ctx.send(response.json())


## get private discord token
client.run(os.getenv('DISCORD_TOKEN'))

## get besttime api private key
## url = f"https://besttime.app/api/v1/keys/{os.getenv('BEST_TIME_PRIVATE_KEY')}"
## response = requests.request("GET", url)
## print(response.json())
