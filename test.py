from dotenv import load_dotenv
from os import getenv
from cogs.classes.client import Client

load_dotenv()

if __name__ == '__main__':
    client = Client(getenv('RIOT_API_KEY'))
    client.debug = True # will print when making API calls

    summoner = client.get_summoner('Mintybadger515')
    champions = summoner.masteries

    match = summoner.matches(limit=1)[0]

    if match.participants.index(summoner) < 5:
        print('team 1')
    else:
        print('team 2')