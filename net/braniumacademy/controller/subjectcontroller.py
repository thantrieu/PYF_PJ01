import json


class ISubjectController:
    pass


class SubjectController(ISubjectController):
    pass


class SubjectJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
