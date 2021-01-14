import requests
from time import sleep

from .rank import Rank
from .summoner import Summoner

class Client:
    def __init__(self, riot_token):
        self.session = requests.session()
        self.route = 'euw1.api.riotgames.com'
        self.headers = {
            'X-Riot-Token' : riot_token
        }


    def _get(self, url, max_retries=5, retry_after=2):
        if not hasattr(self, 'session'):
            self.session =  requests.session()

        retries=0
        while retries<max_retries:
            r = requests.get(url=url, headers=self.headers)
            if 200<=r.status_code<300:
                return r.json()
            sleep(retry_after)


    def get_summoner(self, n: str):
        r = self._get(f'https://{self.route}/lol/summoner/v4/summoners/by-name/{n}')
        if r:
            return Summoner(r)


    def get_rank(self, s: Summoner):
        r = self._get(f'https://{self.route}/lol/league/v4/entries/by-summoner/{s.id}')
        print(r)
        if r:
            return Rank(r)