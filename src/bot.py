import os

import discord
from discord.ext import commands

class BirdBot:
  def __init__(self, token):
    self.token = token
    self.bot = commands.Bot(command_prefix='-')
    self.bot.load_extension("birds")
    self.on_ready = self.bot.event(self.on_ready)

  def run(self):
    self.bot.run(self.token)


  async def on_ready(self):
    print(f'{self.bot.user} has connected to Discord!')
 
if __name__ == "__main__":
  bird = BirdBot(os.environ.get('BIRD_BOT_TOKEN'))
  bird.run()
