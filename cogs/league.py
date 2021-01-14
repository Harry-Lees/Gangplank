from .classes.client import Client
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime, timedelta
from uuid import uuid1
from os import remove
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
from os import getenv

matplotlib.use('Agg')

def setup(bot):
    bot.add_cog(League(bot))


class League(commands.Cog, name='League'):
    def __init__(self, b):
        self.bot = b
        self.client = Client(getenv('RIOT_API_KEY'))

    @commands.command(name='profile')
    async def profile(self, ctx, *s: str):
        if len(s)>1:
            s=' '.join(s)
        else:
            s=s[0]

        async with ctx.typing():
            summoner = self.client.get_summoner(s)
            champions = summoner.top_champions()