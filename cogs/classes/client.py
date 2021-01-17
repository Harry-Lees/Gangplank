import requests
from time import sleep
from typing import Optional, Generator

from .data_classes import *
from .values import *

class Client:
    def __init__(self, token: str, debug: bool = False, default_region: str = 'euw1'):
        self.session = requests.session()
        self.headers = {"X-Riot-Token": token}
        self.debug = debug
        self.default_region = default_region

        # Static API data only calls API once.
        self.champion_constants = StaticChampions(self.champion_constants())

    def build_url(self, endpoint: str, region: Optional[str] = None) -> str:
        if region is None:
            region = self.default_region

        if (region not in REGIONS) and (region not in PLATFORMS):
            raise ValueError(f'Invalid route code {region}')

        end = ENDPOINTS[endpoint]
        base = BASE.format(region=region)
        return base + end

    def get(self, url: str, max_retries: int = 5, retry_after: float = 2) -> Optional[dict]:
        if self.debug:
            print(f"getting {url}")

        if not hasattr(self, "session"):
            self.session = requests.session()

        retries = 0
        while retries < max_retries:
            r = requests.get(url=url, headers=self.headers)
            if 200 <= r.status_code < 300:
                return r.json()
            sleep(retry_after)

    def get_summoner(self, n: str, region: Optional[str] = None, via='name') -> Optional[Summoner]:
        if via not in ('name', 'id', 'account'):
            raise ValueError('via must be name, id, account')

        url = self.build_url(f'summoner_by_{via}', region)
        r = self.get(url.format(n))
        if r:
            return Summoner(r, self)

    def get_ranks(self, s: Summoner) -> Optional[Ranks]:
        url = self.build_url('ranks', region)
        r = self.get(url)
        if r:
            return Ranks(r, self)

    def gen_matches(self, s: Summoner) -> Generator[Match, None, None]:
        matchlist = self.get_matchlist(s)

        for match in matchlist:
            temp = match.get("gameId")
            if temp:
                yield Match(match)

    def get_matches(self, s: Summoner, limit=100) -> Matches:
        matchlist = self.get_matchlist(s)

        matches = []
        n = 0
        for match in matchlist:
            temp = match.get('gameId')
            n += 1
            if temp:
                matches.append(self.get_match(temp))
            if n == limit:
                break

        return Matches(matches, self)

    def get_matchlist(self, s: Summoner) -> dict:
        matches = self.get(ENDPOINTS['matchlist']).get("matches")
        return matches

    def get_match(self, match_id: str) -> dict:
        match = self.get(ENDPOINTS['match'])
        return match

    def champion_constants(self, override: bool = False) -> dict:
        if hasattr(self, "static_champion_data") and not override:
            return self.static_champion_data

        return self.get(ENDPOINTS['dd_champions']).get('data')

    def get_masteries(self, s: Summoner, region: Optional[str] = None) -> Masteries:
        url = self.build_url('masteries', region)
        masteries = self.get(url)

        return Masteries(masteries, self)

    def get_status(self, region: Optional[str] = None) -> dict:
        url = self.build_url('status', region)
        status = self.get(url)

        return status