import tkinter as tk
from tkinter.messagebox import showerror, showinfo, askyesno

from net.braniumacademy.controller.registercontroller import RegisterController
from net.braniumacademy.controller.studentcontroller import StudentController
from net.braniumacademy.controller.subjectcontroller import SubjectController
from net.braniumacademy.utils import *


class RegisterView:
    def __init__(self, master):
        super().__init__()
        self.btn_statistic = None
        self.img_statistic = None
        self.img_chart = None
        self.btn_draw_chart = None
        self.frame = master
        self.btn_search = None
        self.search_entry = None
        self.search_var = None
        self.img_search = None
        self.sort_var = None
        self.tbl_register = None
        self.btn_remove = None
        self.img_remove = None
        self.btn_edit = None
        self.img_edit = None
        self.btn_reload = None
        self.img_refresh = None
        self.subjects = []
        self.students = []
        self.registers = []
        self.controller = RegisterController()
        self.create_widgets()
        self.create_buttons()
        self.load_data()

    def create_widgets(self):
        columns = ('reg_id', 'subject_id', 'subject_name', 'student_id',
                   'student_name', 'reg_time')
        self.tbl_register = ttk.Treeview(self.frame, columns=columns,
                                         show='headings', height=10)
        self.tbl_register.grid(row=0, column=0, columnspan=3,
                               sticky=tk.NSEW, pady=4, padx=4)
        set_style(self.tbl_register)
        # show heading
        self.tbl_register.heading('reg_id', text='Mã đăng ký')
        self.tbl_register.heading('subject_id', text='Mã môn học')
        self.tbl_register.heading('subject_name', text='Tên môn học')
        self.tbl_register.heading('student_id', text='Mã sinh viên')
        self.tbl_register.heading('student_name', text='Họ và tên')
        self.tbl_register.heading('reg_time', text='Thời gian đăng ký')
        # config columns
        self.tbl_register.column(0, stretch=tk.NO, width=120, anchor=tk.CENTER)
        self.tbl_register.column(1, stretch=tk.NO, width=160, anchor=tk.W)
        self.tbl_register.column(2, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_register.column(3, stretch=tk.NO, width=160, anchor=tk.CENTER)
        self.tbl_register.column(4, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_register.column(5, stretch=tk.NO, width=220, anchor=tk.W)
        # add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                  command=self.tbl_register.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS)
        self.tbl_register['yscrollcommand'] = scrollbar.set
        # add buttons
        self.create_search_frame()
        self.create_sort_frame()
        self.create_statistic_frame()

    def create_search_frame(self):
        self.search_var = tk.StringVar()
        frm_search = ttk.LabelFrame(self.frame, text='Tìm kiếm')
        # config set all columns have same width space
        frm_search.columnconfigure(0, weight=1, uniform='fred')
        frm_search.columnconfigure(1, weight=1, uniform='fred')
        frm_search.grid(row=1, column=0, sticky=tk.NSEW, pady=4, padx=4)
        # add combobox
        ttk.Label(frm_search, text='Tiêu chí tìm kiếm:'). \
            grid(row=0, column=0, sticky=tk.W, pady=4, padx=4)
        ttk.Combobox(frm_search, values=search_register_criterias,
                     textvariable=self.search_var). \
            grid(row=1, column=0, padx=4, pady=4, sticky=tk.W,
                 ipady=4, ipadx=4)
        # add search part
        ttk.Label(frm_search, text='Từ khóa:'). \
            grid(row=0, column=1, sticky=tk.W, padx=4, pady=4)
        self.search_entry = ttk.Entry(frm_search)
        self.search_entry.grid(row=1, column=1, sticky=tk.EW, padx=4, pady=4,
                               ipadx=4, ipady=4)
        path = 'view/assets/search_24.png'
        self.img_search = tk.PhotoImage(file=path)
        self.btn_search = ttk.Button(frm_search, text='Tìm kiếm',
                                     image=self.img_search, compound=tk.LEFT,
                                     command=self.btn_search_clicked, width=15)
        self.btn_search.grid(row=2, column=1, padx=4, pady=4)

    def create_sort_frame(self):
        self.sort_var = tk.IntVar(value=0)
        frm_sort = ttk.LabelFrame(self.frame, text='Sắp xếp bản đăng ký')
        frm_sort.columnconfigure(0, weight=1, uniform='fred')
        frm_sort.columnconfigure(1, weight=1, uniform='fred')
        frm_sort.grid(row=1, column=1, sticky=tk.NSEW, pady=4, padx=4)
        # add radio button to this frame
        ttk.Radiobutton(frm_sort, text='Thứ tự đăng ký sớm-muộn', value=1,
                        variable=self.sort_var,
                        command=self.item_sort_by_register_time_asc). \
            grid(row=0, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Thứ tự đăng ký muộn-sớm',
                        value=2, variable=self.sort_var,
                        command=self.item_sort_by_register_time_desc). \
            grid(row=1, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo mã môn học tăng dần',
                        value=3, variable=self.sort_var,
                        command=self.item_sort_by_subject_id_selected). \
            grid(row=0, column=1, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo mã sinh viên tăng dần',
                        value=4, variable=self.sort_var,
                        command=self.item_sort_by_student_id_selected). \
            grid(row=1, column=1, pady=4, padx=4, sticky=tk.W)

    def create_statistic_frame(self):
        frm_statistic = ttk.LabelFrame(self.frame, text='Thống kê')
        # config set all columns have same width space
        frm_statistic.columnconfigure(0, weight=1, uniform='fred')
        frm_statistic.columnconfigure(1, weight=1, uniform='fred')
        frm_statistic.rowconfigure(0, weight=1, uniform='fred')
        frm_statistic.rowconfigure(1, weight=1, uniform='fred')
        frm_statistic.rowconfigure(2, weight=1, uniform='fred')
        frm_statistic.grid(row=1, column=2, sticky=tk.NSEW, pady=4, padx=4)
        chart_icon_path = 'view/assets/chart.png'
        stat_icon_path = 'view/assets/stat.png'
        self.img_chart = tk.PhotoImage(file=chart_icon_path)
        self.img_statistic = tk.PhotoImage(file=stat_icon_path)
        self.btn_statistic = ttk.Button(frm_statistic, text='Thống kê',
                                        image=self.img_statistic, compound=tk.LEFT,
                                        command=self.btn_statistic_clicked, width=15)
        self.btn_draw_chart = ttk.Button(frm_statistic, text='Vẽ biểu đồ',
                                         image=self.img_chart, compound=tk.LEFT,
                                         command=self.btn_draw_chart_clicked, width=15)
        self.btn_statistic.grid(row=1, column=0, padx=4, pady=4)
        self.btn_draw_chart.grid(row=1, column=1, padx=4, pady=4)

    def create_buttons(self):
        button_frame = ttk.LabelFrame(self.frame, text='Các thao tác')
        button_frame.columnconfigure(0, weight=1, uniform='fred')
        button_frame.columnconfigure(1, weight=1, uniform='fred')
        button_frame.columnconfigure(2, weight=1, uniform='fred')
        button_frame.grid(row=2, column=0, columnspan=3,
                          padx=4, pady=4, sticky=tk.NSEW)
        self.img_refresh = tk.PhotoImage(file='view/assets/refresh.png')
        self.btn_reload = ttk.Button(button_frame, text='Làm mới', width=20,
                                     command=self.load_data, image=self.img_refresh,
                                     compound=tk.LEFT)
        self.btn_reload.grid(row=0, column=0, ipady=4, ipadx=4, pady=4, padx=4)
        self.img_edit = tk.PhotoImage(file='view/assets/editing.png')
        self.btn_edit = ttk.Button(button_frame, text='Sửa bản đăng ký', width=20,
                                   command=self.btn_edit_subject_clicked,
                                   image=self.img_edit, compound=tk.LEFT)
        self.btn_edit.grid(row=0, column=1, ipady=4, ipadx=4, pady=4, padx=4)
        self.img_remove = tk.PhotoImage(file='view/assets/remove.png')
        self.btn_remove = ttk.Button(button_frame, text='Xóa bỏ', width=20,
                                     command=self.btn_remove_clicked,
                                     image=self.img_remove, compound=tk.LEFT)
        self.btn_remove.grid(row=0, column=2, ipadx=4, ipady=4, pady=4, padx=4)

    def load_data(self, should_show=True):
        self.subjects.clear()
        self.students.clear()
        if len(self.subjects) == 0:
            self.students = StudentController().read_file(STUDENT_FILE_NAME)
            self.subjects = SubjectController().read_file(SUBJECT_FILE_NAME)
        self.registers = self.controller.read_file(REGISTER_FILE_NAME, self.students, self.subjects)
        if should_show:
            self.show_registers()

    def show_registers(self):
        clear_treeview(self.tbl_register)
        index = 1
        self.tbl_register.selection_clear()
        for register in self.registers:
            if index % 2 == 0:
                tag = 'even'
            else:
                tag = 'odd'
            self.tbl_register.insert('', tk.END,
                                     values=register_to_tuple(register),
                                     tags=(tag,), iid=f'{index - 1}')
            index += 1

    def btn_statistic_clicked(self):
        pass

    def btn_draw_chart_clicked(self):
        pass

    def btn_remove_clicked(self):
        registers = self.controller.read_file(REGISTER_FILE_NAME, self.students, self.subjects)
        item_selected = self.tbl_register.selection()
        if len(item_selected) > 0:
            title = 'Confirmation'
            message = 'Do you want to delete item(s) selected?'
            ans = askyesno(title, message)
            if ans:
                index = int(item_selected[0])
                register_id = self.registers[index].register_id
                self.controller.remove(self.registers, register_id)  # xóa phần tử trong danh sách sinh viên
                self.controller.remove(registers, register_id)  # xóa phần tử trong danh sách nguyên bản
                self.tbl_register.delete(item_selected[0])  # xóa phần tử trong bảng
                self.controller.write_file(REGISTER_FILE_NAME, registers)  # update file
                showinfo(title='Infomation', message=f'Delete register id "{register_id}" successfully!')
        else:
            showerror(title='Error', message='Please select a register to delete first!')

    def btn_edit_subject_clicked(self):
        item_selected = self.tbl_register.selection()
        if len(item_selected) > 0:
            index = int(item_selected[0])  # convert iid from str to int
            # EditSubjectView(self, self.registers[index]).attributes('-topmost', True)
        else:
            showerror(title='Error', message='Please select a subject to edit first!')
        pass

    def create_register(self, subject: Subject):
        self.registers.append(subject)
        self.show_registers()

    def item_save_selected(self):
        self.controller.write_file(REGISTER_FILE_NAME, self.registers)

    def btn_search_clicked(self):
        key = self.search_entry.get()
        criteria = self.search_var.get()
        if len(key) == 0:
            showerror('Invalid keyword', 'Please enter keyword first!')
        elif len(criteria) == 0:
            showerror('Invalid criteria', 'Please select criteria to search!')
        else:
            if criteria == search_register_criterias[0]:
                if is_student_id_valid(key):
                    self.find_by_student_id(key)
                else:
                    showerror('Invalid student id', 'Student id must in the form SV####')
            elif criteria == search_register_criterias[1]:
                if is_subject_id_valid(key):
                    self.find_by_subject_id(int(key))
                else:
                    showerror('Invalid subject_id', 'Subject id must be integer number 4 digits')

    def item_sort_by_register_time_asc(self):
        self.controller.sort_by_register_time_asc(self.registers)
        self.show_registers()

    def item_sort_by_register_time_desc(self):
        self.controller.sort_by_register_time_desc(self.registers)
        self.show_registers()

    def item_sort_by_subject_id_selected(self):
        self.controller.sort_by_subject_id(self.registers)
        self.show_registers()

    def item_sort_by_student_id_selected(self):
        self.controller.sort_by_student_id(self.registers)
        self.show_registers()

    def find_by_student_id(self, key: str):
        self.load_data(False)  # reload data from file
        result = self.controller.find_by_student_id(self.registers, key)
        self.check_result(result)

    def find_by_subject_id(self, key: int):
        self.load_data(False)  # reload subject
        result = self.controller.find_by_subject_id(self.registers, key)
        self.check_result(result)

    def check_result(self, result: list[Register]):
        if len(result) == 0:
            self.registers.clear()
            self.show_registers()
            showinfo('Search Result', 'No result found!')
        else:
            self.registers.clear()
            self.registers = result.copy()
            self.show_registers()
