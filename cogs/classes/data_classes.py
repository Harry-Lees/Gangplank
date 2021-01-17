from collections.abc import Mapping
from typing import Optional, Union, List


class cached_property:
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


class RESTObject:
    '''
    Base DataClass for defining data.
    '''

    def __init__(self, d, client=None):
        self.client = client

        for k, v in d.items():
            setattr(self, k, v)

    def __repr__(self):
        return f'<{self.__class__.__name__} object>'

    def str(self):
        return self.__repr__()


class RESTList:
    '''
    Base DataClass for defining List objects.
    '''

    def __init__(self, j, client):
        self.client = client
        if type(j) is not list:
            raise TypeError(f'received type {type(j)}, expected list')

        self._data = j

    def __getitem__(self, i):
        raise NotImplementedError('__getitem__')

    def __repr__(self):
        return f'<{self.__class__.__name__} object len: {len(self._data)}>'

    def __str__(self):
        return '[' + ', '.join(repr(item) for item in self) + ']'

    def __len__(self):
        return len(self._data)


class Team(RESTObject):
    def __init__(self, d, client):
        super().__init__(d)
        self.bans = Champions.from_ids([ban['championId'] for ban in self.bans], client)


class Teams(RESTList):
    def __getitem__(self, i):
        return Team(self._data[i], self.client)


class Participant(RESTObject):
    pass


class Participants(RESTList):
    def __getitem__(self, i) -> Participant:
        return Participant(self._data[i], self.client)


class Match(RESTObject):
    def __init__(self, d, client):
        super().__init__(d, client)
        self.participantIdentities = Summoners(self.participantIdentities, client)
        self.teams = Teams(self.teams, client)
        self.participants = Participants(self.participants, client)

    def __repr__(self):
        return f'<{self.__class__.__name__} id: {self.gameId}>'


class Rank(RESTObject):
    def __repr__(self):
        return f'<{self.__class__.__name__} queue type: {self.queueType}>'


class Matches(RESTList):
    def __getitem__(self, i):
        return Match(self._data[i], self.client)


class Ranks(RESTList):
    def __getitem__(self, i):
        return Rank(self._data[i], self.client)


class Mastery(RESTObject):
    def __init__(self, d, client):
        super().__init__(d, client)
        self.champion = self.client.champion_constants.from_id(self.championId)


class Masteries(RESTList):
    def __getitem__(self, i) -> Mastery:
        return Mastery(self._data[i], self.client)


class Champion(RESTObject):
    def __repr__(self):
        return f'<{self.__class__.__name__} object: {self.name}>'


class Champions(RESTList):  # implemented the other way around to other data classes
    def __init__(self, champions: Champion):
        self._data = champions

    def __str__(self):
        return str(self._data)

    def __getitem__(self, i):
        return self._data[i]

    @classmethod
    def from_ids(cls, ids: List[int], client):
        return cls([client.champion_constants.from_id(id) for id in ids])

    @classmethod
    def from_names(cls, names: List[str], client):
        return cls([client.champion_constants.get(name) for name in names])


class StaticChampions(Mapping):
    '''
    Read only dictionary with static champion information i.e. Champion names and metadata
    '''

    def __init__(self, data):
        self._data = data
        self._id_data = {
            champion.get('key'): champion for _, champion in self._data.items()
        }

    def __getitem__(self, key) -> Champion:
        return Champion(self._data[key])

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> iter:
        return iter(self._data)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} object len: {len(self)}>'

    def from_id(self, key) -> Optional[Champion]:
        id_data = self._id_data.get(str(key))
        if id_data:
            return Champion(id_data)


class Summoner(RESTObject):
    def __repr__(self):
        return f'<{self.__class__.__name__} object summoner: {self.name}>'

    def __eq__(self, other):
        return self.accountId == other.accountId

    def matches(self, limit=10) -> Matches:
        return self.client.get_matches(self, limit=limit)

    @cached_property
    def masteries(self) -> Masteries:
        return self.client.get_masteries(self)

    @cached_property
    def ranks(self) -> Ranks:
        return self.client.get_ranks(self)

    def iter_matches(self) -> Match:
        yield from self.client.gen_matches(self)


class Summoners(RESTList):
    '''
    to-do: implement caching of summoners to lower number of API calls
    '''

    def __str__(self):
        return '[' + ', '.join(str(self.client.get_summoner_by_id(summoner['player']['currentAccountId'])) for summoner in self._data)+ ']'

    def __getitem__(self, i):
        if isinstance(i, slice):
            return [
                self.client.get_summoner_by_id(
                    self._data[ii]['player']['currentAccountId']
                )
                for ii in range((len(self)))
            ]
        elif isinstance(i, int):
            if i < 0:
                i += len(self)
            if i < 0 or i >= len(self):
                raise IndexError(f'The index {i} is out of range')
        else:
            raise TypeError('Argument must be type int or slice')

        return self.client.get_summoner_by_id(
            self._data[i]['player']['currentAccountId']
        )
