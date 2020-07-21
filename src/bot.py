import argparse
import logging
import os
import sys

import discord
from discord.ext import commands

class BirdBot:
  def __init__(self, token):
    self.token = token
    self.bot = commands.Bot(command_prefix='\\')
    self.bot.load_extension("botcommands")
    self.on_ready = self.bot.event(self.on_ready)

  def run(self):
    self.bot.run(self.token)


  async def on_ready(self):
    logging.info(f'{self.bot.user} has connected to Discord!')
 
def prep_log(debug, console):
  log_format = '%(asctime)s %(funcName)s()_%(lineno)s %(levelname)s: %(message)s'
  date_format = '%m/%d/%Y %I:%M:%S %p'

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  formatter = logging.Formatter(log_format, datefmt=date_format)
  if console:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

  file_handler = logging.FileHandler('logs/log.log')
  file_handler.setLevel(logging.INFO)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)
  
def parser():
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--debug", help="DEBUG MODE", action="store_true")
  parser.add_argument("-c", "--console", help="LOG TO CONSOLE", action="store_true")
  argv = parser.parse_args()

  prep_log(argv.debug, argv.console)
 
if __name__ == "__main__":
  parser()
  bird = BirdBot(os.environ.get('HERM_BOT_TOKEN'))#('BIRD_BOT_TOKEN'))
  bird.run()
