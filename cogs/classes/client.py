import requests
from time import sleep

from .data_classes import *

class Client:
    def __init__(self, riot_token, debug=False):
        self.session = requests.session()
        self.route = 'euw1.api.riotgames.com'
        self.headers = {
            'X-Riot-Token' : riot_token
        }
        self.debug = debug


    def _get(self, url, max_retries=5, retry_after=2):
        if self.debug:
            print(f'getting {url}')

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
            return Summoner(r, self)


    def get_rank(self, s: Summoner):
        r = self._get(f'https://{self.route}/lol/league/v4/entries/by-summoner/{s.id}')
        if r:
            return Rank(r)


    def get_champions(self, s: Summoner):
        masteries = self._get(f'https://{self.route}/lol/champion-mastery/v4/champion-masteries/by-summoner/{s.id}')
        matches = self.get_matches(s)

        if masteries:
            return Champions(masteries, self)


    def get_matches(self, s: Summoner):
        matches = self._get(f'https://{self.route}/lol/match/v4/matchlists/by-account/{s.accountId}').get('matches')
        if matches:
            return Matches(matches, self)