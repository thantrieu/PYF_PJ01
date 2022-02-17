import abc
import json
import re
from abc import abstractmethod

from net.braniumacademy.model.subject import Subject
from net.braniumacademy.utils import decode_subject


class ISubjectController(abc.ABC):
    @abstractmethod
    def create_subject(self, sid: int, name: str,
                       credit: int, lesson: int, category: str) -> Subject:
        pass

    @abstractmethod
    def read_file(self, file_name: str) -> list[Subject]:
        pass

    @abstractmethod
    def update_subject_id(self, current_id: int):
        pass

    @abstractmethod
    def sort_by_subject_id(self, subjects: list[Subject]):
        pass

    @abstractmethod
    def sort_by_subject_name(self, subjects: list[Subject]):
        pass

    @abstractmethod
    def sort_by_subject_credit(self, subjects: list[Subject]):
        pass

    @abstractmethod
    def sort_by_subject_lesson(self, subjects: list[Subject]):
        pass

    @abstractmethod
    def sort_by_subject_category(self, subjects: list[Subject]):
        pass

    @abstractmethod
    def find_by_subject_id(self, subjects: list[Subject],
                           subject_id: int) -> Subject | None:
        pass

    @abstractmethod
    def find_by_subject_name(self, subjects: list[Subject],
                             name: str) -> list[Subject | Subject, ...]:
        pass

    @abstractmethod
    def find_by_subject_credit(self, subjects: list[Subject],
                               credit: int) -> list[Subject | Subject, ...]:
        pass

    @abstractmethod
    def find_by_subject_lesson(self, subjects: list[Subject],
                               lesson: int) -> list[Subject | Subject, ...]:
        pass

    @abstractmethod
    def find_by_subject_category(self, subjects: list[Subject],
                                 category: str) -> list[Subject | Subject, ...]:
        pass


class SubjectController(ISubjectController):
    def find_by_subject_id(self, subjects: list[Subject],
                           subject_id: int) -> Subject | None:
        for subject in subjects:
            if subject.subject_id == subject_id:
                return subject
        return None

    def find_by_subject_name(self, subjects: list[Subject],
                             name: str) -> list[Subject | Subject, ...]:
        result = []
        pattern = f'.*{name}.*'
        for subject in subjects:
            matcher = re.search(pattern, subject.subject_name,
                                flags=re.IGNORECASE)
            if matcher:
                result.append(subject)
        return result

    def find_by_subject_credit(self, subjects: list[Subject],
                               credit: int) -> list[Subject | Subject, ...]:
        result = []
        for subject in subjects:
            if subject.subject_credit == credit:
                result.append(subject)
        return result

    def find_by_subject_lesson(self, subjects: list[Subject],
                               lesson: int) -> list[Subject | Subject, ...]:
        result = []
        for subject in subjects:
            if subject.subject_lesson == lesson:
                result.append(subject)
        return result

    def find_by_subject_category(self, subjects: list[Subject],
                                 category: str) -> list[Subject | Subject, ...]:
        result = []
        pattern = f'.*{category}.*'
        for subject in subjects:
            matcher = re.search(pattern, subject.subject_category,
                                flags=re.IGNORECASE)
            if matcher:
                result.append(subject)
        return result

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

    def sort_by_subject_id(self, subjects: list[Subject]):
        subjects.sort(key=lambda x: x.subject_id)

    def sort_by_subject_name(self, subjects: list[Subject]):
        subjects.sort(key=lambda x: x.subject_name)

    def sort_by_subject_credit(self, subjects: list[Subject]):
        subjects.sort(key=lambda x: x.subject_credit, reverse=True)

    def sort_by_subject_lesson(self, subjects: list[Subject]):
        subjects.sort(key=lambda x: x.subject_lesson)

    def sort_by_subject_category(self, subjects: list[Subject]):
        subjects.sort(key=lambda x: x.subject_category)


class SubjectJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
