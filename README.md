# Crowd Bot for Discord

A simple bot used to query a location and display the current live crowd data

<br>

## Table of Contents
- [Installation](#Installation)
- [Commands](#Commands)
- [APIs](#APIs)


### Installation 

Installing dependencies and packages (Python >=3.5.3 required)
```python
    #For Windows
    py -3 -m pip install -U discord.py
    pip3 install python-dotenv
    pip3 install requests
```
Set up your `.env` variables
```prop
    DISCORD_TOKEN=discord_bot_token
    BT_PRIVATE_KEY=BestTime_private_key
```
#### Commands

- `?help` displays command list
- `?crowd <query>` display live crowd data
- `?magicman <question>` Magic 8Ball
    - also can use `?_8ball`
- `?ping` latency tester


### APIs

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [BestTime](https://besttime.app/)

