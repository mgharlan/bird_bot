from bs4 import BeautifulSoup
import os
import pandas as pd
from pathlib import Path
import random
import requests

import discord
from discord.ext import commands

class Birds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
    self.data = pd.read_csv("bird_data/bird_urls.csv")
      
  @commands.command(name='random')
  async def send_random(self, ctx):
    print('random selected')
    
    number = random.randint(0,self.data.shape[0])
    
    URL = self.data['BIRD URLs'][number]
    bird_name = Path(URL).stem

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
      result = soup.find('div',class_="bird-guide-image")
      img_url = result.find('img')['src']
      img = requests.get(img_url)
      file = open('bird_data/bird.jpg', 'wb')
      file.write(img.content)
      file.close()
      
      image = discord.File(open(f'bird_data/bird.jpg', 'rb'))
      os.remove("bird_data/bird.jpg")
      await ctx.send(file=image)
      
    except Exception as e:
      print(e)
      print(URL, 'problem with image', number)
      await ctx.send(f'**image for {bird_name} not found**')
      if (os.path.exists("bird_data/bird.jpg")):
        os.remove("bird_data/bird.jpg")

    try:
      result = soup.find('div', class_="hide-for-tiny hide-for-small hide-for-medium")
      text = result.text.strip('\t \n')
      await ctx.send(text)
      
    except Exception as e:
      print(e)
      print(URL, 'problem with text', number)
      await ctx.send(f'**text for {bird_name} nor found**')
      
    await ctx.send(f'*From: {URL}*')
    
  @commands.command(name='shutdown')
  async def shut_down(self, ctx):
    print('shut down')
    await ctx.send('Shutting Down')
    await self.bot.logout()

def setup(bot):
  bot.add_cog(Birds(bot))