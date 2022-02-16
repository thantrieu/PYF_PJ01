import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, askyesno, showinfo
from net.braniumacademy.utils import *
from net.braniumacademy.controller.studentcontroller import StudentController
from net.braniumacademy.view.editstudentview import EditStudentView


class StudentView:
    def __init__(self, frame):
        super().__init__()
        self.tbl_student = None
        self.frame = frame
        self.students = []
        self.controller = StudentController()
        self.create_widgets()
        self.load_student()

    def create_widgets(self):
        columns = ('id', 'full_name', 'birth_date',
                   'student_id', 'email', 'address', 'gpa', 'major')
        self.tbl_student = ttk.Treeview(self.frame, columns=columns,
                                        show='headings', height=10)
        self.tbl_student.grid(row=0, column=0, columnspan=3,
                              sticky=tk.NSEW, pady=4, padx=4)
        style = ttk.Style()
        style.theme_use('default')  # other theme can use: clam, classic, default
        style.configure('my.Treeview.Heading', font=('Calibri', 11, 'bold'),
                        background='#6caf50', foreground='#ffffff')
        self.tbl_student.configure(style='my.Treeview')
        # customize style for odd and even row background color
        self.tbl_student.tag_configure('odd', background='#f0f0f0')
        self.tbl_student.tag_configure('even', background='#ffffff')
        # show heading
        self.tbl_student.heading('id', text='CMND/CCCD')
        self.tbl_student.heading('full_name', text='Họ và tên')
        self.tbl_student.heading('birth_date', text='Ngày sinh')
        self.tbl_student.heading('student_id', text='Mã SV')
        self.tbl_student.heading('email', text='Email')
        self.tbl_student.heading('address', text='Địa chỉ')
        self.tbl_student.heading('gpa', text='Điểm TB')
        self.tbl_student.heading('major', text='Chuyên ngành')
        # config columns
        self.tbl_student.column(0, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(1, stretch=tk.NO, width=150, anchor=tk.W)
        self.tbl_student.column(2, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(3, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(4, stretch=tk.NO, width=180, anchor=tk.W)
        self.tbl_student.column(5, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_student.column(6, stretch=tk.NO, width=100, anchor=tk.CENTER)
        self.tbl_student.column(7, stretch=tk.NO, width=150, anchor=tk.W)
        # add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                  command=self.tbl_student.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS)
        self.tbl_student['yscrollcommand'] = scrollbar.set
        # add buttons
        self.create_search_frame()
        self.create_sort_frame()
        self.create_chart_frame()
        self.create_buttons()

    def create_search_frame(self):
        self.search_var = tk.StringVar()
        frm_search = ttk.LabelFrame(self.frame, text='Search by')
        # config set all columns have same width space
        frm_search.columnconfigure(0, weight=1, uniform='fred')
        frm_search.columnconfigure(1, weight=1, uniform='fred')
        frm_search.grid(row=1, column=0, sticky=tk.NSEW, pady=4, padx=4)
        # add combobox
        ttk.Label(frm_search, text='Search criteria:'). \
            grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        ttk.Combobox(frm_search, values=search_criterias,
                     textvariable=self.search_var). \
            grid(row=1, column=0, padx=4, pady=4, sticky=tk.W)
        # add search part
        ttk.Label(frm_search, text='Keyword:'). \
            grid(row=0, column=1, sticky=tk.W, padx=4, pady=4)
        self.search_entry = ttk.Entry(frm_search)
        self.search_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=4)
        ttk.Button(frm_search, text='Search',
                   command=self.search, width=15). \
            grid(row=2, column=1, padx=4, pady=4)

    def create_sort_frame(self):
        self.sort_var = tk.IntVar(value=0)
        frm_sort = ttk.LabelFrame(self.frame, text='Sort by')
        frm_sort.columnconfigure(0, weight=1, uniform='fred')
        frm_sort.columnconfigure(1, weight=1, uniform='fred')
        frm_sort.grid(row=1, column=1, sticky=tk.NSEW, pady=4, padx=4)
        # add radio button to this frame
        ttk.Radiobutton(frm_sort, text='Name a-z', value=1,
                        variable=self.sort_var,
                        command=self.item_sort_by_name_selected). \
            grid(row=0, column=0, pady=4, padx=4)
        ttk.Radiobutton(frm_sort, text='Birth date',
                        value=2, variable=self.sort_var,
                        command=self.item_sort_by_birth_date_selected). \
            grid(row=1, column=0, pady=4, padx=4)
        ttk.Radiobutton(frm_sort, text='Gpa decrement',
                        value=3, variable=self.sort_var,
                        command=self.item_sort_by_gpa_selected). \
            grid(row=0, column=1, pady=4, padx=4)
        ttk.Radiobutton(frm_sort, text='Gpa and name',
                        value=4, variable=self.sort_var,
                        command=self.item_sort_by_gpa_and_name_selected). \
            grid(row=1, column=1, pady=4, padx=4)

    def create_chart_frame(self):
        frm_other = ttk.LabelFrame(self.frame, text='Chart')
        frm_other.grid(row=1, column=2, sticky=tk.NSEW, pady=4, padx=4)
        ttk.Button(frm_other, text='Draw chart', width=20,
                   command=lambda: self.draw_chart()). \
            place(rely=0.5, relx=0.5, anchor=tk.CENTER)

    def create_buttons(self):
        button_frame = ttk.LabelFrame(self.frame, text='Actions')
        button_frame.columnconfigure(0, weight=1, uniform='fred')
        button_frame.columnconfigure(1, weight=1, uniform='fred')
        button_frame.columnconfigure(2, weight=1, uniform='fred')
        button_frame.grid(row=2, column=0, columnspan=3,
                          padx=4, pady=4, sticky=tk.NSEW)
        ttk.Button(button_frame, text='Reload Students', width=20,
                   command=self.load_student). \
            grid(row=0, column=0, ipady=4, ipadx=4, pady=4, padx=4)
        ttk.Button(button_frame, text='Edit GPA', width=20,
                   command=self.btn_edit_student_clicked). \
            grid(row=0, column=1, ipady=4, ipadx=4, pady=4, padx=4)
        ttk.Button(button_frame, text='Remove Items', width=20,
                   command=self.btn_remove_student_clicked). \
            grid(row=0, column=2, ipadx=4, ipady=4, pady=4, padx=4)

    def load_student(self, should_show=True):
        self.students.clear()
        self.students = self.controller.read_file(STUDENT_FILE_NAME)
        if should_show:
            self.show_students()

    def show_students(self):
        clear_treeview(self.tbl_student)
        index = 1
        self.tbl_student.selection_clear()
        for student in self.students:
            if index % 2 == 0:
                tag = 'even'
            else:
                tag = 'odd'
            self.tbl_student.insert('', tk.END,
                                    values=student_to_tuple(student),
                                    tags=(tag,))
            index += 1

    def btn_remove_student_clicked(self):
        item_selected = self.tbl_student.selection()
        if len(item_selected) > 0:
            title = 'Confirmation'
            message = 'Do you want to delete item(s) selected?'
            ans = askyesno(title, message)
            if ans:
                for item in item_selected:
                    index = int(item[1:], 16) - 1  # lấy vị trí hàng cần xóa - 1 có được vị trí phần tử trong danh sách
                    self.controller.remove(self.students, index)  # xóa phần tử trong danh sách sinh viên
                    self.tbl_student.delete(item)  # xóa phần tử trong bảng
                self.controller.write_file(STUDENT_FILE_NAME, self.students)  # update file
                showinfo(title='Infomation', message='Delete successfully!')
        else:
            showerror(title='Error', message='Please select a row to delete first!')

    def btn_edit_student_clicked(self):
        item_selected = self.tbl_student.selection()
        if len(item_selected) > 0:
            item = item_selected[0]
            index = (int(item[1:], 16) - 1) % len(self.students)
            EditStudentView(self, self.students[index]).attributes('-topmost', True)

    def item_create_student_selected(self, student: Student):
        self.students.append(student)
        self.show_students()

    def item_sort_by_name_selected(self):
        self.controller.sort_by_name(self.students)
        # self.students.sort(key=lambda x: (x.full_name.first_name, x.full_name.last_name))
        self.show_students()

    def item_sort_by_birth_date_selected(self):
        self.controller.sort_by_birth_date(self.students)
        self.show_students()

    def item_sort_by_gpa_selected(self):
        self.controller.sort_by_gpa(self.students)
        self.show_students()

    def item_sort_by_gpa_and_name_selected(self):
        self.controller.sort_by_name_gpa(self.students)
        self.show_students()

    def item_save_selected(self):
        self.controller.write_file(STUDENT_FILE_NAME, students=self.students)
        showinfo('Successfully', 'Save students data to file successfully!')

    def draw_chart(self):
        pass

    def search(self):
        key = self.search_entry.get()
        criteria = self.search_var.get()
        if len(key) == 0:
            showerror('Invalid keyword', 'Please enter keyword first!')
        elif len(criteria) == 0:
            showerror('Invalid criteria', 'Please select criteria to search!')
        else:
            if criteria == search_criterias[0]:
                self.search_by_name(key)
            elif criteria == search_criterias[1]:
                self.search_by_gpa(float(key))
            elif criteria == search_criterias[2]:
                self.search_by_birth_date(int(key))
            elif criteria == search_criterias[3]:
                self.search_by_birth_month(int(key))
            elif criteria == search_criterias[4]:
                self.search_by_birth_year(int(key))

    def search_by_name(self, key: str):
        self.load_student(False)  # reload student
        result = self.controller.search_by_name(self.students, key)
        if len(result) == 0:
            self.students.clear()
            self.show_students()
            showinfo('Search Result', 'No result found!')
        else:
            self.students = result.copy()
            self.show_students()

    def search_by_gpa(self, key: float):
        self.load_student(False)  # reload student
        result = self.controller.search_by_gpa(self.students, key)
        if len(result) == 0:
            self.students.clear()
            self.show_students()
            showinfo('Search Result', 'No result found!')
        else:
            self.students = result.copy()
            self.show_students()

    def search_by_birth_date(self, key: int):
        self.load_student(False)  # reload student
        result = self.controller.search_by_birth_date(self.students, key)
        if len(result) == 0:
            self.students.clear()
            self.show_students()
            showinfo('Search Result', 'No result found!')
        else:
            self.students = result.copy()
            self.show_students()

    def search_by_birth_month(self, key: int):
        self.load_student(False)  # reload student
        result = self.controller.search_by_birth_month(self.students, key)
        if len(result) == 0:
            self.students.clear()
            self.show_students()
            showinfo('Search Result', 'No result found!')
        else:
            self.students = result.copy()
            self.show_students()

    def search_by_birth_year(self, key: int):
        self.load_student(False)  # reload student
        result = self.controller.search_by_birth_year(self.students, key)
        if len(result) == 0:
            self.students.clear()
            self.show_students()
            showinfo('Search Result', 'No result found!')
        else:
            self.students = result.copy()
            self.show_students()
