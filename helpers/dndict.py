import json
from typing import Any

class DNDict(dict):
    # Loads a dict object into the class during the initialization
    # Uses custom __getattribute__ methods to allow getting items from the dict via dot notation
    # __dict__ and json properties
    # example usage:
    # t = DNDict({'a': 1})
    # print(t.a)
    # > 1
    # Without this class, it would have to be like the following
    # print(mydict.get('a')) # .get to prevent KeyError
    def __init__(self, obj: dict): self.obj = obj
    def __getattribute__(self, __name: str) -> Any: 
        __value = super().__getattribute__('obj').get(__name)
        return super().__getattribute__(__name) if not __value and hasattr(DNDict, __name) else __value
    @property
    def __dict__(self): return super().__getattribute__('obj')
    @property
    def json(self):return json.dumps(self.__dict__)