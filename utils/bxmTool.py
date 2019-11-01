class BXMDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__
class BXMList(list):
    pass

