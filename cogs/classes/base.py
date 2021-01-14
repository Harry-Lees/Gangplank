class DataClass:
    '''
    Base DataClass that other classes inherit from.
    '''

    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, v)


    def __repr__(self):
        return f'<{self.__class__.__name__} object>'