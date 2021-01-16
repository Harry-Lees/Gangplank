from dotenv import load_dotenv
from os import getenv
from cogs.classes.client import Client

load_dotenv()

if __name__ == '__main__':
    client = Client(getenv('RIOT_API_KEY'))
    client.debug = True # will print when making API calls

    summoner = client.get_summoner('Mintybadger515')
    champions = summoner.masteries

    matches = summoner.matches(limit=10)

    for match in matches:
        for i, participant in enumerate(match.participants):
            s = match.participantIdentities[i]
            if s == summoner:
                team_index = (1, 0)[participant.teamId % 100]
                team = match.teams[team_index]

                print(client.champion_constants.from_id(participant.championId).name, end=' ')
                print(participant.stats['kills'], end=' ')
                print(participant.stats['deaths'], end=' ')
                print(participant.stats['assists'], end=' ')
                print('Won' if team.win == 'Win' else 'Lost')

                break