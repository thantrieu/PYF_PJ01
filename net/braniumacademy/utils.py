from net.braniumacademy.model.student import Student, BirthDate, FullName, Address

STUDENT_FILE_NAME = 'student.json'
SUBJECT_FILE_NAME = 'subject.json'
REGISTER_FILE_NAME = 'register.json'


def student_to_tuple(student: Student) -> tuple[str | str, ...]:
    """ Hàm tiện ích thực hiện chuyển đổi thông tin sinh viên thành một
        tuple chứa các phần tử biểu diễn ở string.
    """
    return tuple([student.person_id, student.full_name,
                  student.birth_date, student.student_id,
                  student.email, student.address,
                  f'{student.gpa:0.2f}', student.major])


def clear_treeview(treeview):
    """ Hàm tiện ích dùng để xóa toàn bộ bản ghi trong bảng(treeview)
        trước khi hiển thị thông tin mới vào đó nhằm tránh trùng lặp các bản ghi.
    """
    for item in treeview.get_children():
        treeview.delete(item)


def create_birth_date(data: str) -> BirthDate:
    items = data.split('/')
    day, month, year = int(items[0]), items[1], items[2]
    return BirthDate(day, month, year)


def decode_full_name(dct):
    if 'first' in dct:
        return FullName(dct['first'], dct['last'], dct['mid'])
    else:
        return dct


def decode_address(dct):
    if 'city' in dct:
        return Address(dct['wards'], dct['district'], dct['city'])
    return dct


def decode_birth_date(dct):
    if 'day' in dct:
        return BirthDate(int(dct['day']), int(dct['month']), int(dct['year']))
    return dct


def decode_student(dct):
    if 'student_id' in dct:
        pid = dct['person_id']
        full_name = decode_full_name(dct['full_name'])
        birth_date = decode_birth_date(dct['birth_date'])
        address = decode_address(dct['address'])
        sid = dct['student_id']
        email = dct['email']
        major = dct['major']
        gpa = float(dct['gpa'])
        return Student(pid, full_name, birth_date, sid, email, address, gpa, major)
    else:
        return dct
