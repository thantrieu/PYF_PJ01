import abc
import datetime
import json
from abc import abstractmethod

from net.braniumacademy.model.register import Register
from net.braniumacademy.model.student import Student
from net.braniumacademy.model.subject import Subject
from net.braniumacademy.utils import decode_register, register_delta_time


class IRegisterController(abc.ABC):
    @abstractmethod
    def write_file(self, file_name: str, registers: list[Register]):
        pass

    @abstractmethod
    def read_file(self, file_name: str, students: list[Student],
                  subjects: list[Subject]) -> list[Register | Register, ...]:
        pass

    @abstractmethod
    def remove(self, registers: list[Register], reg_id: int) -> bool:
        pass

    @abstractmethod
    def add_register(self, reg_id: int, subject: Subject,
                     student: Student) -> Register:
        pass

    @abstractmethod
    def update_register_id(self, student_id):
        pass

    @abstractmethod
    def sort_by_register_time_asc(self, registers: list[Register]):
        pass

    @abstractmethod
    def sort_by_register_time_desc(self, registers: list[Register]):
        pass

    @abstractmethod
    def sort_by_subject_id(self, registers: list[Register]):
        pass

    @abstractmethod
    def sort_by_student_id(self, registers: list[Register]):
        pass

    @abstractmethod
    def find_by_student_id(self, registers: list[Register],
                           student_id: str) -> list[Register | Register, ...]:
        pass

    @abstractmethod
    def find_by_subject_id(self, registers: list[Register],
                           subject_id: int) -> list[Register | Register, ...]:
        pass

    @abstractmethod
    def statistic(self):
        pass

    @abstractmethod
    def updat_register_subject(self, reg: Register,
                               subjects: list[Subject], subject_id: int):
        pass

    @abstractmethod
    def updat_register_student(self, reg: Register,
                               students: list[Student], student_id: str):
        pass


class RegisterController(IRegisterController):
    def updat_register_subject(self, reg: Register,
                               subjects: list[Subject], subject_id: int):
        for subject in subjects:
            if subject.subject_id == subject_id:
                reg.subject = subject
                break

    def updat_register_student(self, reg: Register,
                               students: list[Student], student_id: str):
        for student in students:
            if student.student_id == student_id:
                reg.student = student
                break

    def remove(self, registers: list[Register], reg_id: int) -> bool:
        index = 0
        for subject in registers:
            if subject.register_id == reg_id:
                registers.pop(index)
                return True
            index += 1
        return False

    def add_register(self, reg_id: int, subject: Subject,
                     student: Student) -> Register:
        pass

    def sort_by_register_time_asc(self, registers: list[Register]):
        registers.sort(key=lambda x: register_delta_time(x.register_time))

    def sort_by_register_time_desc(self, registers: list[Register]):
        registers.sort(key=lambda x: register_delta_time(x.register_time), reverse=True)

    def sort_by_subject_id(self, registers: list[Register]):
        registers.sort(key=lambda x: x.subject.subject_id)

    def sort_by_student_id(self, registers: list[Register]):
        registers.sort(key=lambda x: x.student.student_id)

    def find_by_student_id(self, registers: list[Register],
                           student_id: str) -> list[Register | Register, ...]:
        result = []
        for reg in registers:
            if reg.student.student_id == student_id.upper():
                result.append(reg)
        return result

    def find_by_subject_id(self, registers: list[Register],
                           subject_id: int) -> list[Register | Register, ...]:
        result = []
        for reg in registers:
            if reg.subject.subject_id == subject_id:
                result.append(reg)
        return result

    def statistic(self):
        pass

    def write_file(self, file_name: str, registers: list[Register]):
        with open(file_name, 'w', encoding='UTF-8') as writer:
            encoded_data = json.dumps(registers, cls=RegisterJSONEncoder,
                                      indent=2, ensure_ascii=False)
            writer.write(encoded_data)

    def read_file(self, file_name: str, students: list[Student],
                  subjects: list[Subject]) -> list[Register | Register, ...]:
        with open(file_name, encoding='UTF-8') as reader:
            data = reader.read()
            registers = json.loads(data, object_hook=decode_register)
        for reg in registers:
            self.updat_register_subject(reg, subjects, reg.subject)
            self.updat_register_student(reg, students, reg.student)
        registers.sort(key=lambda x: x.register_id)
        self.update_register_id(registers[len(registers) - 1].register_id)
        return registers

    def update_register_id(self, student_id):
        Register.AUTO_ID = student_id + 1


class RegisterJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.to_dict()
