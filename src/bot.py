import logging
import os

import discord

client = discord.Client()

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')

if __name__ == "__main__":
  client.run(os.environ.get('BIRD_BOT_TOKEN'))