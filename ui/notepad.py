import tkinter
import tkinter.scrolledtext
import tkinter.font
import sys

from ui.icons import Icons
from managers.file_manager import FileManager
from managers.preferences_manager import PreferencesManager
from managers.editor_manager import EditorManager

class Notepad:
    def __init__(self):
        self.window = tkinter.Tk()
        self.counters_frame = tkinter.Frame(self.window)
        self.main_frame = tkinter.Frame(self.window)
        self.main_font = tkinter.font.Font(family="DejaVu Sans Mono",
                                           size=16)
        self.text = tkinter.scrolledtext.ScrolledText(self.main_frame,
                                                      font=self.main_font,
                                                      undo=True,
                                                      autoseparators=True)
        self.editor_manager = EditorManager(self)
        self.file_manager = FileManager(self)
        self.file_manager.add_editor_manager(self.editor_manager)
        self.editor_manager.add_file_manager(self.file_manager)
        self.preferences_manager = PreferencesManager(self)
        self.characters_count_label = tkinter.Label(self.counters_frame,
                                                      font=self.main_font,
                                                      text=f"Characters: {self.editor_manager.characters_count}")
        self.words_count_label = tkinter.Label(self.counters_frame,
                                               font=self.main_font,
                                               text=f"Words: {self.editor_manager.words_count}")
        self.line_number_label = tkinter.Label(self.counters_frame,
                                              font=self.main_font,
                                              text=f"Line: {self.editor_manager.line_number}")
        self.column_number_label = tkinter.Label(self.counters_frame,
                                              font=self.main_font,
                                              text=f"Column: {self.editor_manager.column_number}")
        self.menu_bar = tkinter.Menu(self.window,
                                     font=self.main_font)
        self.file_menu = tkinter.Menu(self.menu_bar,
                                      tearoff=tkinter.OFF,
                                      font=self.main_font)
        self.edit_menu = tkinter.Menu(self.menu_bar,
                                      tearoff=tkinter.OFF,
                                      font=self.main_font)
        self.icons = Icons()
        self.appearance_menu = tkinter.Menu(self.menu_bar,
                                            tearoff=tkinter.OFF,
                                            font=self.main_font)
        self.font_family_menu = tkinter.Menu(self.appearance_menu,
                                             tearoff=tkinter.OFF,
                                             font=self.main_font)
        self.font_style_menu = tkinter.Menu(self.appearance_menu,
                                            tearoff=tkinter.OFF,
                                            font=self.main_font)
        self.themes_menu = tkinter.Menu(self.appearance_menu,
                                        tearoff=tkinter.OFF,
                                        font=self.main_font)

    def maximize_window(self) -> None:
        if sys.platform == "linux":
            self.window.attributes("-zoomed", True)
        elif sys.platform == "win32":
            self.window.state("zoomed")

    def initialize(self) -> None:
        self.window.title("Notepad--")
        self.window.iconphoto(True, self.icons.app_icon)
        self.window.config(menu=self.menu_bar,
                           bg="#000000")
        self.window.protocol("WM_DELETE_WINDOW", self.file_manager.exit)
        self.menu_bar.add_cascade(label="File",
                                  menu=self.file_menu)
        self.file_menu.add_command(label="New",
                                   command=self.file_manager.new_file,
                                   image=self.icons.new_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + N")
        self.file_menu.add_command(label="Open",
                                   command=self.file_manager.open_file,
                                   image=self.icons.open_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + O")
        self.file_menu.add_command(label="Save",
                                   command=self.file_manager.save_file,
                                   image=self.icons.save_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + S")
        self.file_menu.add_command(label="Save As...",
                                   command=self.file_manager.save_file_as,
                                   image=self.icons.save_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + Shift + S")
        self.file_menu.add_command(label="Auto Save",
                                   command=self.file_manager.toggle_auto_save,
                                   image=self.icons.auto_save_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Alt + A")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",
                                   command=self.file_manager.exit,
                                   image=self.icons.exit_icon,
                                   compound=tkinter.LEFT)
        self.menu_bar.add_cascade(label="Edit",
                            menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo",
                                   accelerator="Ctrl + Z",
                                   command=self.editor_manager.undo,
                                   image=self.icons.undo_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Redo",
                                   accelerator="Ctrl + Y",
                                   command=self.editor_manager.redo,
                                   image=self.icons.redo_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Clear",
                                   command=self.editor_manager.clear_file,
                                   image=self.icons.clear_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + Shift + Delete")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut",
                                   accelerator="Ctrl + X",
                                   command=self.editor_manager.cut,
                                   image=self.icons.cut_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Copy",
                                   accelerator="Ctrl + C",
                                   command=self.editor_manager.copy,
                                   image=self.icons.copy_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Paste",
                                   accelerator="Ctrl + V",
                                   command=self.editor_manager.paste,
                                   image=self.icons.paste_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find",
                                   command=self.editor_manager.find,
                                   image=self.icons.find_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + F")
        self.edit_menu.add_command(label="Find & Replace",
                                   command=self.editor_manager.find_and_replace,
                                   image=self.icons.find_and_replace_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + H")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Generate Random Text",
                                   command=self.editor_manager.generate_random_text,
                                   image=self.icons.generate_random_text_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + G")
        self.edit_menu.add_command(label="Toggle Word Wrap",
                                   command=self.preferences_manager.toggle_word_wrap,
                                   image=self.icons.word_wrap_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Alt + Z")
        self.font_style_menu.add_command(label="Normal",
                                          command=lambda: self.preferences_manager.change_font_style("normal"))
        self.font_style_menu.add_command(label="Bold",
                                          command=lambda: self.preferences_manager.change_font_style("bold"))
        self.font_style_menu.add_separator()
        self.font_style_menu.add_command(label="Roman",
                                          command=lambda: self.preferences_manager.change_font_style("roman"))
        self.font_style_menu.add_command(label="Italic",
                                         command=lambda: self.preferences_manager.change_font_style("italic"))
        self.menu_bar.add_cascade(label="Appearance",
                                  menu=self.appearance_menu)
        self.appearance_menu.add_command(label="Reset",
                                         command=self.preferences_manager.set_preferences_to_default,
                                         image=self.icons.reset_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Themes",
                                         command=self.preferences_manager.manage_themes,
                                         image=self.icons.themes_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Background Color",
                                         command=self.preferences_manager.change_background_color,
                                         image=self.icons.change_background_color_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Font Color",
                                         command=self.preferences_manager.change_font_color,
                                         image=self.icons.change_font_color_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Font Family",
                                         image=self.icons.change_font_family_icon,
                                         compound=tkinter.LEFT,
                                         command=self.preferences_manager.change_font_family)
        self.appearance_menu.add_cascade(label="Change Font Style",
                                         menu=self.font_style_menu,
                                         image=self.icons.change_font_style_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Font Size",
                                         command=self.preferences_manager.change_font_size,
                                         image=self.icons.change_font_size_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_separator()
        self.appearance_menu.add_command(label="Save Preferences",
                                         command=self.preferences_manager.save_preferences,
                                         image=self.icons.save_file_icon,
                                         compound=tkinter.LEFT)
        self.text.pack(expand=True, fill=tkinter.BOTH)
        self.characters_count_label.grid(row=0, column=0, pady=5, padx=5)
        self.words_count_label.grid(row=0, column=1, padx=75, pady=5)
        self.line_number_label.grid(row=0, column=2, padx=5, pady=5)
        self.column_number_label.grid(row=0, column=3, padx=75, pady=5)
        self.counters_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.window.bind("<KeyRelease>", self.editor_manager.update_footer_stats)
        self.main_frame.pack(expand=True, fill=tkinter.BOTH)
        self.preferences_manager.load_themes()
        self.preferences_manager.load_preferences()
        self.window.update()
        self.maximize_window()
        self.window.bind("<Control-h>", self.editor_manager.find_and_replace)
        self.window.bind("<Control-f>", self.editor_manager.find)
        self.window.bind("<Control-s>", self.file_manager.save_file)
        self.window.bind("<Control-Shift-S>", self.file_manager.save_file_as)
        self.window.bind("<Control-n>", self.file_manager.new_file)
        self.window.bind("<Control-o>", self.file_manager.open_file)
        self.window.bind("<Alt-z>", self.preferences_manager.toggle_word_wrap)
        self.window.bind("<Control-Shift-Delete>", self.editor_manager.clear_text)
        self.window.bind("<Control-g>", self.editor_manager.generate_random_text)
        self.window.bind("<Control-a>", self.editor_manager.select_all)
        self.window.bind("<Alt-a>", self.file_manager.toggle_auto_save)
        self.window.mainloop()

if __name__ == "__main__":
    notepad = Notepad()
    notepad.initialize()