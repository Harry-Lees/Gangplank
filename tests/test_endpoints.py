import sys
import pytest
from os import getenv
from dotenv import load_dotenv

sys.path.append('..')
from cogs.classes.client import Client
from cogs.classes.data_classes import *

load_dotenv()

def test_summoner():
    client = Client(getenv('RIOT_API_KEY'))
    client.debug = True
    
    summoner = client.get_summoner('GoingQuantum10')
    assert type(summoner) == Summoner

def test_matches():
    pass