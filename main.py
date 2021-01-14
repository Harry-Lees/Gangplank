import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()

bot = commands.Bot(command_prefix = '!')

__author__ = 'Harry Lees'
__credits__ = ['Harry Lees', 'Siddhant Jogai']
__status__ = 'Production'

bot.load_extension('cogs.league')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')

    await bot.change_presence(
        activity = discord.Activity(
            type = discord.ActivityType.playing,
            name = 'League of Legends'
        )
    )

if __name__ == '__main__':
    bot.run(getenv('DISCORD_BOT_TOKEN'))