from os import getenv
from typing import Union, List

from discord import Colour, Embed
from discord.ext import commands

from .classes.client import Client


def setup(bot):
    bot.add_cog(League(bot))


class League(commands.Cog, name='League'):
    def __init__(self, b):
        self.bot = b
        self.client = Client(getenv('RIOT_API_KEY'))

    @commands.command(name='profile')
    async def profile(self, ctx, *, s: str):
        async with ctx.typing():
            summoner = self.client.get_summoner(s)
        await ctx.send('command not implemented yet')

    @commands.command(name='status')
    async def status(self, ctx: object, region: str):
        async with ctx.typing():
            status = self.client.get_status(region)

            e = Embed(
                title=f'Status for {region.upper()}',
                colour=Colour.blue()
            )

            for incident in status.incidents:
                e.add_field(name='Status', value=incident['maintenance_status'])
                e.add_field(name='Description', value=incident['updates'][-1]['translations'][0]['content'][:1024]) # this field has the possibility of exceeding the character limit so it's manually limited to 1024
                e.add_field(name='Severity', value=incident['incident_severity'])

            for maintenance in status.maintenances:
                e.add_field(name='Status', value=maintenance['maintenance_status'])
                e.add_field(name='Description', value=maintenance['updates'][-1]['translations'][0]['content'][:1024])
                e.add_field(name='Severity', value='N/A')

        await ctx.send(embed=e)

    @commands.command(name='chests')
    async def available_chests(self, ctx, *, s: str):
        async with ctx.typing():
            summoner = self.client.get_summoner(s)
            masteries = summoner.masteries

            embed = Embed(
                title=f'Available Chests for {s}',
                description='Sorted by champion mastery (limit 10)',
                colour=Colour.blue(),
            )
            champions = [c.champion.name for c in masteries if not c.chestGranted]
            embed.add_field(name='Champion', value='\n'.join(champions[:10]))

            await ctx.send(embed=embed)

    @commands.command(name='match_history')
    async def match_history(self, ctx, *, s: str):
        async with ctx.typing():
            summoner = self.client.get_summoner(s)
            matches = summoner.matches(limit=10)

            champion, kda, outcome = [], [], []
            for match in matches:
                for i, participant in enumerate(match.participants):
                    temp_summoner = match.participantIdentities[i]
                    if temp_summoner == summoner:
                        team_index = (1, 0)[participant.teamId % 100] # convert 100, 200 to 1 or 0
                        team = match.teams[team_index]

                        champion.append(
                            self.client.champion_constants.from_id(
                                participant.championId
                            ).name
                        )
                        kda.append(
                            '/'.join(
                                [
                                    str(participant.stats['kills']),
                                    str(participant.stats['deaths']),
                                    str(participant.stats['assists']),
                                ]
                            )
                        )
                        outcome.append('Victory' if team.win == 'Win' else 'Defeat')

                        break

            embed = Embed(
                title=f'Match History for {s}',
                description='Most recent matches shown first (limit 10)',
                colour=Colour.blue(),
            )

            embed.add_field(
                name='Champion', value='\n'.join(c for c in champion), inline=True
            )
            embed.add_field(name='kda', value='\n'.join(k for k in kda), inline=True)
            embed.add_field(
                name='Win', value='\n'.join(o for o in outcome), inline=True
            )

            await ctx.send(embed=embed)
