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
from typing import Union, List

#embed.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/11.1.1/img/profileicon/{summoner.profileIconId}.png')

matplotlib.use('Agg')

def setup(bot):
    bot.add_cog(League(bot))


class League(commands.Cog, name='League'):
    def __init__(self, b):
        self.bot = b
        self.client = Client(getenv('RIOT_API_KEY'))

    @staticmethod
    def sanitise_name(s: Union[str, list]) -> str:
        if len(s)>1:
            return ' '.join(s)
        else:
            return s[0]

    @commands.command(name='profile')
    async def profile(self, ctx, *s: str):
        s = self.sanitise_name(s)

        async with ctx.typing():
            summoner = self.client.get_summoner(s)
        ctx.send('command not implemented yet')

    @commands.command(name='chests')
    async def available_chests(self, ctx, *s: List[str]):
        s = self.sanitise_name(s)

        async with ctx.typing():
            summoner = self.client.get_summoner(s)
            masteries = summoner.masteries
            
            embed = discord.Embed(title=f'Available Chests for {s}', description='Sorted by champion mastery (limit 10)', colour=discord.Colour.blue())
            champions = [c.champion.name for c in masteries if not c.chestGranted]
            embed.add_field(name='Champion', value='\n'.join(champions[:10]))

            await ctx.send(embed=embed)

    @commands.command(name='match_history')
    async def match_history(self, ctx, *s: List[str]):
        s = self.sanitise_name(s)

        async with ctx.typing()
            summoner = self.client.get_summoner(s)
            matches = summoner.matches

            embed = discord.Embed(title=f'Match History', description='Most recent matches shown first (limit 10)', colour=discord.Colour.blue())
            
            embed.add_field(name='Champion Played', value='', inline=True)
            embed.add_field(name='Won', value='', inline=True)
            embed.add_field(name='Game Type', value='', inline=True)