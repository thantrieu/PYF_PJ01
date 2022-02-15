import tkinter as tk
from tkinter import ttk

from net.braniumacademy.controller.subjectcontroller import SubjectController


class SubjectView(tk.Tk):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        self.controller = SubjectController()
        self.create_widgets()
        self.load_subject()

    def create_widgets(self):
        pass

    def load_subject(self):
        pass

    def show_subjects(self):
        pass

    def remove_subject(self):
        pass

    def edit_subject(self):
        pass

    def create_subject(self):
        pass

    def item_sort_by_name_selected(self):
        pass

    def item_sort_by_credit_selected(self):
        pass

    def item_search_by_subject_name_selected(self):
        pass

    def item_search_by_credit_selected(self):
        pass

    def item_search_by_category_selected(self):
        pass
