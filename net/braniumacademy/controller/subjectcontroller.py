import abc
import json
from abc import abstractmethod

from net.braniumacademy.model.subject import Subject
from net.braniumacademy.utils import decode_subject


class ISubjectController(abc.ABC):
    @abstractmethod
    def create_subject(self, sid: int, name: str, credit: int, lesson: int, category: str) -> Subject:
        pass

    @abstractmethod
    def read_file(self, file_name: str) -> list[Subject]:
        pass

    @abstractmethod
    def update_subject_id(self, current_id: int):
        pass


class SubjectController(ISubjectController):
    def read_file(self, file_name: str) -> list[Subject]:
        with open(file_name, encoding='UTF-8') as reader:
            data = reader.read()
            subjects = json.loads(data, object_hook=decode_subject)
        subjects.sort(key=lambda x: x.subject_id)
        self.update_subject_id(subjects[len(subjects) - 1].subject_id)
        return subjects

    def update_subject_id(self, current_id: int):
        if current_id != 0:
            Subject.AUTO_ID = current_id + 1

    def create_subject(self, sid: int, name: str, credit: int, lesson: int, category: str) -> Subject:
        pass


class SubjectJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
