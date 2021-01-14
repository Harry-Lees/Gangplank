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


class RESTList(RESTObject):
    '''
    Base DataClass for defining List objects.
    '''

    def __init__(self, j, client):
        self.client = client
        if type(j) is not list:
            raise TypeError(f'received type {type(j)}, expected list')

        self._data = j
        for l in j:
            for k, v in l.items():
                setattr(self, k, v)


    def __getitem__(self, i):
        raise NotImplementedError('__getitem__')


    def __repr__(self):
        return f'<{self.__class__.__name__} object len: {len(self._data)}>'


class Summoner(RESTObject):
    @cached_property
    def matches(self):
        x = self.client.get_matches(self)
        print(x)
        return x

    @cached_property
    def top_champions(self):
        return self.client.get_champions(self)

    def __repr__(self):
        return f'<{self.__class__.__name__} object summoner: {self.name}>'


class Champion(RESTObject):
    pass


class Match(RESTObject):
    pass


class Rank(RESTObject):
    pass


class Champions(RESTList):
    def __getitem__(self, i):
        return Champion(self._data[i], self.client)


class Matches(RESTList):
    def __getitem__(self, i):
        return Match(self._data[i], self.client)


class Ranks(RESTList):
    def __getitem__(self, i):
        return Rank(self._data[i], self.client)