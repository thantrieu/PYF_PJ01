import tkinter as tk
from tkinter import ttk

from net.braniumacademy.controller.subjectcontroller import SubjectController
from net.braniumacademy.utils import *


class SubjectView:
    def __init__(self, frame):
        super().__init__()
        self.btn_search = None
        self.search_entry = None
        self.search_var = None
        self.img_search = None
        self.sort_var = None
        self.tbl_subject = None
        self.btn_remove = None
        self.img_remove = None
        self.btn_edit = None
        self.img_edit = None
        self.btn_reload = None
        self.img_refresh = None
        self.subjects = []
        self.frame = frame
        self.controller = SubjectController()
        self.create_widgets()
        self.create_buttons()
        self.load_subject()

    def create_widgets(self):
        columns = ('subject_id', 'subject_name', 'subject_credit',
                   'subject_lesson', 'subject_category')
        self.tbl_subject = ttk.Treeview(self.frame, columns=columns,
                                        show='headings', height=10)
        self.tbl_subject.grid(row=0, column=0, columnspan=3,
                              sticky=tk.NSEW, pady=4, padx=4)
        style = ttk.Style()
        style.theme_use('default')  # other theme can use: clam, classic, default
        style.configure('my.Treeview.Heading', font=('Calibri', 11, 'bold'),
                        background='#6caf50', foreground='#ffffff')
        self.tbl_subject.configure(style='my.Treeview')
        # customize style for odd and even row background color
        self.tbl_subject.tag_configure('odd', background='#f0f0f0')
        self.tbl_subject.tag_configure('even', background='#ffffff')
        # show heading
        self.tbl_subject.heading('subject_id', text='Mã môn học')
        self.tbl_subject.heading('subject_name', text='Tên môn học')
        self.tbl_subject.heading('subject_credit', text='Số tín chỉ')
        self.tbl_subject.heading('subject_lesson', text='Số tiết học')
        self.tbl_subject.heading('subject_category', text='Loại môn học')
        # config columns
        self.tbl_subject.column(0, stretch=tk.NO, width=220, anchor=tk.CENTER)
        self.tbl_subject.column(1, stretch=tk.NO, width=220, anchor=tk.W)
        self.tbl_subject.column(2, stretch=tk.NO, width=220, anchor=tk.CENTER)
        self.tbl_subject.column(3, stretch=tk.NO, width=220, anchor=tk.CENTER)
        self.tbl_subject.column(4, stretch=tk.NO, width=220, anchor=tk.W)
        # add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL,
                                  command=self.tbl_subject.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS)
        self.tbl_subject['yscrollcommand'] = scrollbar.set
        # add buttons
        self.create_search_frame()
        self.create_sort_frame()

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
        ttk.Combobox(frm_search, values=search_subject_criterias,
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
                                     command=self.search, width=15)
        self.btn_search.grid(row=2, column=1, padx=4, pady=4)

    def create_sort_frame(self):
        self.sort_var = tk.IntVar(value=0)
        frm_sort = ttk.LabelFrame(self.frame, text='Sắp xếp')
        frm_sort.columnconfigure(0, weight=1, uniform='fred')
        frm_sort.columnconfigure(1, weight=1, uniform='fred')
        frm_sort.grid(row=1, column=1, sticky=tk.NSEW, pady=4, padx=4)
        # add radio button to this frame
        ttk.Radiobutton(frm_sort, text='Theo mã môn học a-z', value=1,
                        variable=self.sort_var,
                        command=self.item_sort_by_id_selected). \
            grid(row=0, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo tên môn học a-z',
                        value=2, variable=self.sort_var,
                        command=self.item_sort_by_name_selected). \
            grid(row=1, column=0, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo số tín chỉ giảm dần',
                        value=3, variable=self.sort_var,
                        command=self.item_sort_by_credit_selected). \
            grid(row=0, column=1, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo số tiết học tăng dần',
                        value=4, variable=self.sort_var,
                        command=self.item_sort_by_lesson_selected). \
            grid(row=1, column=1, pady=4, padx=4, sticky=tk.W)
        ttk.Radiobutton(frm_sort, text='Theo loại môn học a-z',
                        value=5, variable=self.sort_var,
                        command=self.item_sort_by_category_selected). \
            grid(row=1, column=1, pady=4, padx=4, sticky=tk.W)

    def create_buttons(self):
        button_frame = ttk.LabelFrame(self.frame, text='Các thao tác')
        button_frame.columnconfigure(0, weight=1, uniform='fred')
        button_frame.columnconfigure(1, weight=1, uniform='fred')
        button_frame.columnconfigure(2, weight=1, uniform='fred')
        button_frame.grid(row=2, column=0, columnspan=2,
                          padx=4, pady=4, sticky=tk.NSEW)
        self.img_refresh = tk.PhotoImage(file='view/assets/refresh.png')
        self.btn_reload = ttk.Button(button_frame, text='Làm mới', width=20,
                                     command=self.load_subject, image=self.img_refresh,
                                     compound=tk.LEFT)
        self.btn_reload.grid(row=0, column=0, ipady=4, ipadx=4, pady=4, padx=4)
        self.img_edit = tk.PhotoImage(file='view/assets/editing.png')
        self.btn_edit = ttk.Button(button_frame, text='Sửa điểm TB', width=20,
                                   command=self.btn_edit_subject_clicked,
                                   image=self.img_edit, compound=tk.LEFT)
        self.btn_edit.grid(row=0, column=1, ipady=4, ipadx=4, pady=4, padx=4)
        self.img_remove = tk.PhotoImage(file='view/assets/remove.png')
        self.btn_remove = ttk.Button(button_frame, text='Xóa bỏ', width=20,
                                     command=self.btn_remove_subject_clicked,
                                     image=self.img_remove, compound=tk.LEFT)
        self.btn_remove.grid(row=0, column=2, ipadx=4, ipady=4, pady=4, padx=4)

    def load_subject(self, should_show=True):
        self.subjects.clear()
        self.subjects = self.controller.read_file(SUBJECT_FILE_NAME)
        if should_show:
            self.show_subjects()

    def show_subjects(self):
        clear_treeview(self.tbl_subject)
        index = 1
        self.tbl_subject.selection_clear()
        for subject in self.subjects:
            if index % 2 == 0:
                tag = 'even'
            else:
                tag = 'odd'
            self.tbl_subject.insert('', tk.END,
                                    values=subject_to_tuple(subject),
                                    tags=(tag,), iid=f'{index - 1}')
            index += 1

    def btn_remove_subject_clicked(self):
        pass

    def btn_edit_subject_clicked(self):
        pass

    def create_subject(self):
        pass

    def search(self):
        pass

    def item_sort_by_id_selected(self):
        pass

    def item_sort_by_name_selected(self):
        pass

    def item_sort_by_credit_selected(self):
        pass

    def item_sort_by_lesson_selected(self):
        pass

    def item_sort_by_category_selected(self):
        pass

    def item_search_by_subject_name_selected(self):
        pass

    def item_search_by_credit_selected(self):
        pass

    def item_search_by_category_selected(self):
        pass
