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
    async def available_chests(self, ctx, *, s):
        # s = self.sanitise_name(s)

        async with ctx.typing():
            summoner = self.client.get_summoner(s)
            masteries = summoner.masteries
            
            embed = discord.Embed(title=f'Available Chests for {s}', description='Sorted by champion mastery (limit 10)', colour=discord.Colour.blue())
            champions = [c.champion.name for c in masteries if not c.chestGranted]
            embed.add_field(name='Champion', value='\n'.join(champions[:10]))

            await ctx.send(embed=embed)

    @commands.command(name='match_history')
    async def match_history(self, ctx, *, s: str):
        # s = self.sanitise_name(s)

        async with ctx.typing():
            summoner = self.client.get_summoner(s)
            matches = summoner.matches(limit=10)

            champion, kda, outcome = [], [], []
            for match in matches:
                for i, participant in enumerate(match.participants):
                    temp_summoner = match.participantIdentities[i]
                    if temp_summoner == summoner:
                        team_index = (1, 0)[participant.teamId % 100]
                        team = match.teams[team_index]

                        champion.append(self.client.champion_constants.from_id(participant.championId).name)
                        kda.append('/'.join([str(participant.stats['kills']), str(participant.stats['deaths']), str(participant.stats['assists'])]))
                        outcome.append('Victory' if team.win == 'Win' else 'Defeat')

                        break

            embed = discord.Embed(title=f'Match History for {s}', description='Most recent matches shown first (limit 10)', colour=discord.Colour.blue())
            
            embed.add_field(name='Champion', value='\n'.join(c for c in champion), inline=True)
            embed.add_field(name='kda', value='\n'.join(k for k in kda), inline=True)
            embed.add_field(name='Win', value='\n'.join(o for o in outcome), inline=True)

            await ctx.send(embed=embed)