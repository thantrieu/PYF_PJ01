import abc
import json


class IRegisterController(abc.ABC):
    pass


class RegisterController(IRegisterController):
    pass


class StudentJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
