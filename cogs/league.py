from .classes.client import Client
from config import Config
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime, timedelta
from uuid import uuid1
from os import remove
import matplotlib
import matplotlib.pyplot as plt
import sqlite3

matplotlib.use('Agg')

def setup(bot):
    bot.add_cog(League(bot))


class League(commands.Cog, name='League'):
    def __init__(self, b):
        self.bot = b
        self.client = Client(Config.RIOT_API_KEY)

    @commands.command(name = 'profile')
    async def profile(self, ctx, *summoner: str):
        if len(summoner)>1:
            summoner = ' '.join(summoner)
        else:
            summoner = summoner[0]

        filename = f'{uuid1()}.png'
        author = ctx.message.author
        guild = author.guild

        async with ctx.typing():
            summoner = self.client.get_summoner(summoner)

            if summoner:
                rank = self.client.get_rank(summoner)

                if rank:
                    with sqlite3.connect('summoners.db') as connection:
                        cursor = connection.cursor()
                        cursor.execute('select * from summoner where id = :summoner_id', {'summoner_id':summoner.id})
                        if not cursor.fetchone():
                            cursor.execute('insert into summoner values(:summoner_name, :summoner_id)', {'summoner_id':summoner.id, 'summoner_name':summoner.name})
            else:
                ctx.send('The summoner provided does not exist')

            if rank:
                e = discord.Embed(title=f'{summoner.name}\'s profile', colour=discord.Colour.blue())
                e.set_thumbnail(url=f'http://ddragon.leagueoflegends.com/cdn/11.1.1/img/profileicon/{summoner.profileIconId}.png')

                e.set_image(url='attachment://image.png')
                e.add_field(name='Rank', value = f'{rank.tier} {rank.rank}')
                e.add_field(name='LP', value = rank.leaguePoints)
                e.add_field(name='Winrate', value=f'{round(rank.wins/(rank.losses+rank.wins)*100, 2)}%')
                e.add_field(name='Hot Streak', value=rank.hotStreak, inline=False)

                with sqlite3.connect('summoners.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute('select timestamp, lp from gains inner join summoner on summoner.id = gains.summoner_id where summoner.name = :summoner_name', {'summoner_name':summoner.name})
                    
                    r = cursor.fetchall()
                    print(r)

                    if r:
                        timestamp, lp = zip(*r)

                        fig, ax = plt.subplots()
                        ax.plot(timestamp, lp)
                        ax.set_ylabel('LP (Cumulative)')
                        ax.set_xlabel('Date')
                        ax.set_title('LP gain/loss (total)')
                        ax.grid(True)

                        # fig.autofmt_xdate()
                        fig.tight_layout()
                        fig.savefig(filename)

                        file = discord.File(filename, filename='image.png')

                        await ctx.send(file=file, embed=e)
                        remove(filename)
                    else:
                        e.add_field(name='LP Graph', value='Not enough data to display')
                        await ctx.send(embed=e)
            else:
                e = discord.Embed(title=f'{summoner.name} is unranked', colour=discord.Colour.red())
                await ctx.send(embed=e)
