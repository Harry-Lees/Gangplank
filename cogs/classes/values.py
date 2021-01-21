from locale import getlocale

BASE = 'https://{region}.api.riotgames.com/'
LOCALE = getlocale()[0].replace('_', '-')
REGIONS = ('americas', 'asia', 'europe')

PLATFORMS = (
    'br1',
    'eun1',
    'euw1',
    'jp1',
    'kr',
    'la1',
    'la2',
    'na1',
    'oc1',
    'tr1',
    'ru'
)

ENDPOINTS = {
    'dd_champions'                          : 'http://ddragon.leagueoflegends.com/cdn/11.1.1/data/en_US/champion.json',
    'matchlist'                             : 'lol/match/v4/matchlists/by-account/{}',
    'match_by_id'                           : 'lol/match/v4/matches/{}',
    'rank_by_summoner'                      : 'lol/league/v4/entries/by-summoner/{}',
    'status'                                : 'lol/status/v4/platform-data',
    'summoner_by_id'                        : 'lol/summoner/v4/summoners/by-puuid/{}',
    'summoner_by_name'                      : 'lol/summoner/v4/summoners/by-name/{}',
    'summoner_by_account'                   : 'lol/summoner/v4/summoners/by-account/{}',
    'masteries_by_summoner'                 : '/lol/champion-mastery/v4/champion-masteries/by-summoner/{}',
    'masteries_by_summoner_by_champion'     : '/lol/champion-mastery/v4/champion-masteries/by-summoner/{}/by-champion/{}',
    'total_mastery_by_summoner'             : '/lol/champion-mastery/v4/scores/by-summoner/{}',
    'status'                                : '/lol/status/v4/platform-data'
}

HEADERS = {'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8'}