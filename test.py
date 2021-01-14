from dotenv import load_dotenv
from os import getenv
from cogs.classes.client import Client


load_dotenv()

if __name__ == '__main__':
    client = Client(getenv('RIOT_API_KEY'))
    client.debug = True

    summoner = client.get_summoner('GoingQuantum10')
    matches = summoner.matches

    print(matches[0].__dict__)