from cogs.classes.client import Client
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()

rank_offset = 100
rank = {
    'IV' : 0*rank_offset,
    'III': 1*rank_offset,
    'II' : 2*rank_offset,
    'I'  : 3*rank_offset,
}

tier_offset = 400
tier = {
    'IRON'          : 0*tier_offset,
    'BRONZE'        : 1*tier_offset,
    'SILVER'        : 2*tier_offset,
    'GOLD'          : 3*tier_offset,
    'PLATINUM'      : 4*tier_offset,
    'DIAMOND'       : 5*tier_offset,
    'MASTER'        : 6*tier_offset,
    'GRANDMASTER'   : 7*tier_offset,
    'CHALLENGER'    : 8*tier_offset
}

if __name__ == '__main__':
    client = Client(getenv('RIOT_API_KEY'))

    with sqlite3.connect('summoners.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM summoner')

        for summoner_name, summoner_id in cursor.fetchall():
            s = client.get_summoner(summoner_name)
            r = client.get_rank(s)

            total_lp = r.leaguePoints + rank[r.rank] + tier[r.tier]
            params = {
                'summoner_id'   : summoner_id,
                'timestamp'     : datetime.now().strftime('%Y-%m-%d %X'),
                'lp'            : total_lp
            }

            cursor.execute('INSERT INTO gains VALUES(:summoner_id, :timestamp, :lp)', params)