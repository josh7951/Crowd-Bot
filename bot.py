import os
import datetime
import requests
import discord 
import random

from discord import channel
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands, timers

load_dotenv(find_dotenv())

client = commands.Bot(command_prefix = '?')
client.remove_command('help')
client.timer_manager = timers.TimerManager(client)

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
    embed.add_field(name="flipcoin", value="Flips a coin", inline=False)
    embed.add_field(name="magicman <question>", value="Magic 8Ball\nalso can use `?8ball`", inline=False)
    embed.add_field(name="remind <Year/Month/Day> <reminder>", value="Remind you to do something!", inline=False)
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
async def test(ctx, *, query):
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

@client.command()
async def flipcoin(ctx):
    choices = ["Heads", "Tails"]
    coin_flip = random.choice(choices)
    await ctx.send(coin_flip)

@client.command()
async def remind(ctx, time, *, text):
    """Data must be in ``Y/M/D`` format."""
    date = datetime.datetime(*map(int, time.split("/")))

    client.timer_manager.create_timer("reminder", date, args=(ctx.channel.id, ctx.author.id, text))

@client.event
async def on_reminder(channel_id, author_id, text):
    channel = client.get_channel(channel_id)

    await channel.send("Hey, <@{0}>, don't forget to: {1}".format(author_id, text))
    insult = [ "Skuzz Ball",
               "Slooze",
               "Fatass",
               "Dirty Cuck"]

    await channel.send(f"You {random.choice(insult)}")

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
    ## JSON OBJECT THAT IS RETURNED if SUCCESSFUL
    # {'analysis': {'hour_end': 14, 'hour_end_12': '2PM', 'hour_start': 13, 'hour_start_12': '1PM', 'note': "parameter 'venue_live_forecasted_detla' is deprecated, and replaced by 'venue_live_forecasted_delta'", 'venue_forecasted_busyness_available': False, 'venue_live_busyness': 50, 'venue_live_busyness_available': True, 'venue_live_forecasted_delta': 'Not available'}, 'status': 'OK', 'venue_info': {'venue_address': '37217 47th St E Palmdale, CA 93552 United States', 'venue_current_gmttime': 'Sunday 2021-06-27 08:18PM', 'venue_current_localtime': 'Sunday 2021-06-27 01:18PM', 'venue_id': 'ven_344b344f7950625f53423652416f77346e4a763379395f4a496843', 'venue_name': "McDonald's", 'venue_open': 'Closed', 'venue_timezone': 'America/Los_Angeles'}}
    ## JSON OBJECT THAT IS RETURNED IF UNSUCCESSFUL
    # {'message': 'Venue not found', 'status': 'error', 'venue_address': 'palmdale', 'venue_name': 'mcdonalds'}

    response = requests.request("POST", url, params=params)
    crowd_json = response.json()
    
    if 'message' in crowd_json and crowd_json['message'] == 'Venue not found':
        await ctx.send('Error: Venue not found. Please check your spelling or be more specific with the address!')
    else:
        if crowd_json['analysis']['venue_live_busyness_available'] == True:

            crowd_val = crowd_json['analysis']['venue_live_busyness']
            
            await ctx.send(f"Current Crowd index: {crowd_val}")
            if crowd_val < 15:
                await ctx.send("It's a ghost town!")
            elif 15 <= crowd_val < 30:
                await ctx.send("There's a small crowd but it's still pretty empty")
            elif 30 <= crowd_val < 60:
                await ctx.send("It's getting a little busy")
            elif 60 <= crowd_val < 75:
                await ctx.send("It's pretty busy!")
            else:
                await ctx.send("It's packed!!")   
        else:
            await ctx.send(f"Error: No Crowd Data available - location may be closed")

## get private discord token
client.run(os.getenv('DISCORD_TOKEN'))