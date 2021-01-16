import requests
from time import sleep

from .data_classes import *
from .values import *


class Client:
    def __init__(self, token, locale=LOCALE,debug=False):
        self.session = requests.session()
        self.route = 'euw1.api.riotgames.com'
        self.headers = {'X-Riot-Token':token}
        self.debug = debug

        # Static API data only calls API once.
        self.champion_constants = StaticChampions(self._champion_constants())

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

    def get_summoner(self, n: str) -> Summoner:
        r = self._get(f'https://{self.route}/lol/summoner/v4/summoners/by-name/{n}')
        if r:
            return Summoner(r, self)

    def get_summoner_by_id(self, id: str) -> Summoner:
        r = self._get(f'https://{self.route}/lol/summoner/v4/summoners/by-account/{id}')
        if r:
            return Summoner(r, self)

    def get_ranks(self, s: Summoner) -> Ranks:
        r = self._get(f'https://{self.route}/lol/league/v4/entries/by-summoner/{s.id}')
        if r:
            return Ranks(r, self)

    def recently_played(self, s: Summoner) -> None:
        matches = self.get_matche
    
    def gen_matches(self, s: Summoner) -> Match:
        matchlist = self._get_matchlist(s)

        for match in matchlist:
            temp = match.get('gameId')
            if temp:
                yield Match(match)

    def get_matches(self, s: Summoner, limit=100) -> Matches:
        matchlist = self._get_matchlist(s)

        matches = []
        n = 0
        for match in matchlist:
            temp = match.get('gameId')
            n += 1
            if temp:
                matches.append(self._get_match(temp))
            if n == limit:
                break

        return Matches(matches, self)

    def _get_matchlist(self, s: Summoner) -> dict:
        matches = self._get(f'https://{self.route}/lol/match/v4/matchlists/by-account/{s.accountId}').get('matches')
        return matches

    def _get_match(self, match_id: str) -> dict:
        match = self._get(f'https://{self.route}/lol/match/v4/matches/{match_id}')
        return match

    def _champion_constants(self, override=False):
        if hasattr(self, 'static_champion_data') and not override:
            return self.static_champion_data

        return self._get('http://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/champion.json').get('data')

    def get_masteries(self, s: Summoner):
        masteries = self._get(f'https://{self.route}/lol/champion-mastery/v4/champion-masteries/by-summoner/{s.id}')
        return Masteries(masteries, self)