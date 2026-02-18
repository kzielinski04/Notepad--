import tkinter
import os

class Icons:
    def __init__(self):
        self.new_file_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/new_file_icon.png"))
        self.open_file_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/open_file_icon.png"))
        self.save_file_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/save_file_icon.png"))
        self.app_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/app_icon.png"))
        self.exit_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/exit_icon.png"))
        self.change_font_family_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/change_font_family_icon.png"))
        self.clear_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/clear_icon.png"))
        self.reset_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/reset_icon.png"))
        self.change_background_color_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/change_background_color_icon.png"))
        self.change_font_color_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/change_font_color_icon.png"))
        self.change_font_size_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/change_font_size_icon.png"))
        self.change_font_style_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/change_font_style_icon.png"))
        self.find_and_replace_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/find_and_replace_icon.png"))
        self.generate_random_text_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/generate_random_text_icon.png"))
        self.themes_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/themes_icon.png"))
        self.word_wrap_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/word_wrap_icon.png"))
        self.find_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/find_icon.png"))
        self.cut_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/cut_icon.png"))
        self.copy_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/copy_icon.png"))
        self.paste_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/paste_icon.png"))
        self.undo_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/undo_icon.png"))
        self.redo_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/redo_icon.png"))
        self.auto_save_icon = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "../assets/auto_save_icon.png"))