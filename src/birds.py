import os
from pathlib import Path
import random

import discord
from discord.ext import commands

class Birds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
    #generate bird set
    self.birds = set()
    bird_data = Path(os.getcwd()+'/bird_data/')
    for path in bird_data.iterdir():
      self.birds.add(path.stem)
      
  @commands.command(name='random')
  async def send_random(self, ctx):
    bird = random.sample(self.birds,1)[0]
    file = open(f'bird_data/{bird}.txt')
    text = file.read()
    await ctx.send(text)

def setup(bot):
  bot.add_cog(Birds(bot))