from .base import DataClass

class Rank(DataClass):
    def __init__(self, d):
        for k, v in d[0].items():
            setattr(self, k, v)