from bs4 import BeautifulSoup
import logging
import os
import pandas as pd
from pathlib import Path
import random
import requests

import discord
from discord.ext import commands

class BotCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
    self.data = pd.read_csv("bird_data/bird_urls.csv")
      
  @commands.command(name='r', aliases=['random'], brief='for random bird facts')
  async def send_random(self, ctx):
    logging.info(f'{ctx.author.name} selected random')
    
    await ctx.send('gathering random bird...')
    
    number = random.randint(0,self.data.shape[0])
    
    URL = self.data['BIRD URLs'][number]
    
    await self.send_bird(ctx, URL)
  
  @commands.command(name='l', aliases=['list'], brief='list birds that start with the letter provided')
  async def list(self, ctx, *args):
    if (len(args) == 0):
      await ctx.send('please provide a first letter to list by')
    elif (len(args) == 1 and args[0].isalpha()):
      bird_string = ''
      searching = True
      sent = False
      for URL in self.data['BIRD URLs']:
        name = Path(URL).stem
        if name[0] == args[0]:
          if len(bird_string) > 1500:
            await ctx.send(f'birds that begin with {args[0]}:' + bird_string)
            sent = True
            bird_string = f'\t\t{name}'
          else:
            bird_string = bird_string + f'\n\t{name}'
          searching = False
        elif not searching:
          break
      if (len(bird_string) == 0):
        await ctx.send(f'no birds begin with {args[0]}')
      elif sent:
        await ctx.send(bird_string)
      else:
        await ctx.send(f'birds that begin with {args[0]}:' + bird_string)
    else:
      await ctx.send('please provide one first letter to list by')
  
  @commands.command(name='show', brief='show the bird specified')
  async def show(self, ctx, *args):
    if (len(args) == 0):
      await ctx.send('please provide a bird to show')
    elif (len(args) == 1):
      name = args[0].lower()
      sent = False
      for URL in self.data['BIRD URLs']:
        if Path(URL).stem == name:
          await ctx.send('gathering bird...')
          await self.send_bird(ctx, URL)
          sent = True
          break
      if not sent:
        await ctx.send(f'bird {name} was not found in my database')
    else:
      await ctx.send('please provide one bird to show')
  
  @commands.command(name='f', aliases=['search','find'], brief='searches for birds')
  async def search(self, ctx, *args):
    if (len(args) == 0):
      await ctx.send('please provide a word/phrase to search for')
    else:
      sent = False
      for arg in args:
        names = ''
        phrase = arg.lower()
        for URL in self.data['BIRD URLs']:
          name = Path(URL).stem
          if phrase in name:
            names = names +f'\n\t{name}'
          if len(names) > 1500:
            if not sent:
              sent = True
              await ctx.send(f'these birds matched the search for {arg}:' + names)
              names = ''
            else:
              await ctx.send(names)
              names = ''
        if len(names) == 0:
          await ctx.send(f'no birds matched the search for {phrase} in my database')
        elif not sent:
          await ctx.send(f'these birds matched the search for {arg}:' + names)
  
  async def send_bird(self, ctx, URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    bird_name = Path(URL).stem

    try:
      result = soup.find('div',class_="bird-guide-image")
      img_url = result.find('img')['src']
      img = requests.get(img_url)
      file = open('bird_data/bird.jpg', 'wb')
      file.write(img.content)
      file.close()
      
      image = discord.File(open('bird_data/bird.jpg', 'rb'))
      os.remove("bird_data/bird.jpg")
      await ctx.send(file=image)
      
    except Exception as e:
      logging.error(e, exc_info=True)
      logging.info(URL + ', problem with bird image')
      await ctx.send(f'**image for {bird_name} not found**')
      if (os.path.exists("bird_data/bird.jpg")):
        os.remove("bird_data/bird.jpg")

    try:
      result = soup.find('div', class_="hide-for-tiny hide-for-small hide-for-medium")
      text = result.text.strip('\t \n')
      await ctx.send(text)
      
    except Exception as e:
      logging.error(e, exc_info=True)
      logging.info(URL + ', problem with bird text')
      await ctx.send(f'**text for {bird_name} not found**')
      
    await ctx.send(f'*From: {URL}*')
  
  @commands.command(name='s', aliases=['shutdown'], hidden=True)
  async def shut_down(self, ctx):
    if(ctx.author.name == 'mazonly' or ctx.author.name == 'ruby 🌻'):
      logging.info('shut down')
      await ctx.send('Shutting Down')
      await self.bot.logout()
    else:
      await ctx.send('no!')

def setup(bot):
  bot.add_cog(BotCommands(bot))
