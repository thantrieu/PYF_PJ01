import tkinter as tk
from tkinter import ttk, Menu
from net.braniumacademy.view.addnewstudentview import AddNewStudentView
from net.braniumacademy.view.studentview import StudentView


class HomeView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('QUẢN LÝ ĐĂNG KÝ MÔN HỌC')
        self.resizable(False, False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.menubar = Menu()
        self.configure(menu=self.menubar)
        self.iconbitmap('./view/assets/icon.ico')
        self.create_notebook()
        self.create_student_view()
        self.create_menu()

    def create_notebook(self):
        notebook = ttk.Notebook()
        notebook.grid(row=0, column=0, sticky=tk.NSEW)
        # add student frame
        self.frm_student = ttk.Frame(notebook)
        # cấu hình cho các cột của frame có cùng độ rộng
        self.frm_student.columnconfigure(0, weight=1, uniform='fred')
        self.frm_student.columnconfigure(1, weight=1, uniform='fred')
        self.frm_student.columnconfigure(2, weight=1, uniform='fred')
        self.frm_student.grid(row=0, column=0)
        # add subject frame
        self.frm_subject = ttk.Frame(notebook)
        self.frm_subject.rowconfigure(0, weight=4)
        self.frm_subject.rowconfigure(1, weight=1)
        self.frm_subject.columnconfigure(0, weight=3)
        self.frm_subject.columnconfigure(1, weight=3)
        self.frm_subject.columnconfigure(2, weight=3)
        self.frm_subject.columnconfigure(3, weight=1)
        self.frm_subject.grid(row=0, column=0)
        # add register frame
        self.frm_register = ttk.Frame(notebook)
        self.frm_register.rowconfigure(0, weight=4)
        self.frm_register.rowconfigure(1, weight=1)
        self.frm_register.columnconfigure(0, weight=1)
        self.frm_register.columnconfigure(1, weight=1)
        self.frm_register.columnconfigure(2, weight=1)
        self.frm_register.grid(row=0, column=0)
        # add frame to notebook
        notebook.add(self.frm_student, text='Student Managerment')
        notebook.add(self.frm_subject, text='Subject Managerment')
        notebook.add(self.frm_register, text='Register Managerment')

    def create_menu(self):
        file_menu = Menu(self.menubar, tearoff=False)
        submenu_file = Menu(file_menu, tearoff=False)
        submenu_file.add_command(label='Student',
                                 command=lambda: self.create_student())
        submenu_file.add_command(label='Subject',
                                 command=lambda: self.create_subject())
        submenu_file.add_command(label='Register',
                                 command=lambda: self.create_register())
        file_menu.add_cascade(label='Create New...',
                              underline=0, menu=submenu_file)
        # save menu item
        file_menu.add_command(label='Save', command=lambda: self.save())
        # other menu items
        file_menu.add_separator()
        file_menu.add_command(label='Exit', underline=0, command=self.destroy)
        # add to menu bar
        self.menubar.add_cascade(label='File', menu=file_menu, underline=0)
        self.menubar.add_cascade(label='Help', underline=0)
        self.menubar.add_cascade(label='Settings', underline=0)

    def create_student_view(self):
        self.student_view = StudentView(self.frm_student)

    def create_student(self):
        popup = AddNewStudentView(self.student_view)
        popup.attributes('-topmost', True)  # showing popup alway on top of master frame
        popup.mainloop()

    def save(self):
        self.student_view.item_save_selected()

    def create_subject(self):
        pass

    def create_register(self):
        pass
