import tkinter
import tkinter.messagebox
import tkinter.font
import tkinter.colorchooser
import json
import os

class PreferencesManager:
    def __init__(self, notepad):
        self.preferences_file_path = os.path.join(os.path.dirname(__file__), "../settings/preferences.json")
        self.themes_file_path = os.path.join(os.path.dirname(__file__), "../settings/themes.json")
        self.saved_preferences = {}
        self.word_wrap_on = False
        self.themes = []
        self.notepad = notepad
        self.default_themes_count = 9

    def toggle_word_wrap(self, event=None) -> None:
        if self.word_wrap_on:
            self.word_wrap_on = False
            self.notepad.text.config(wrap=tkinter.NONE)
            tkinter.messagebox.showinfo(title="Word Wrap OFF", message="Word Wrap is now disabled")
        else:
            self.word_wrap_on = True
            self.notepad.text.config(wrap=tkinter.WORD)
            tkinter.messagebox.showinfo(title="Word Wrap ON", message="Word Wrap is now enabled")

    def change_background_color(self) -> None:
        color = tkinter.colorchooser.askcolor(title="Change Background Color")[1]
        self.notepad.text.config(bg=color)

    def change_font_color(self) -> None:
        color = tkinter.colorchooser.askcolor(title="Change Font Color")[1]
        self.notepad.text.config(fg=color)

    def save_preferences(self) -> None:
        current_font = tkinter.font.Font(font=self.notepad.text["font"])
        selection_background_color = self.notepad.text["selectbackground"]
        selection_foreground_color = self.notepad.text["selectforeground"]
        background_color = self.notepad.text["bg"]
        font_color = self.notepad.text["fg"]
        font_family = current_font["family"]
        font_weight = current_font["weight"]
        font_size = current_font["size"]
        font_weight = current_font["weight"]
        font_slant = current_font["slant"]
        preferences = {
            "background_color": background_color,
            "font_color": font_color,
            "selection_background_color": selection_background_color,
            "selection_foreground_color": selection_foreground_color,
            "font_family": font_family,
            "font_weight": font_weight,
            "font_slant": font_slant,
            "font_size": font_size,
            "word_wrap_on": self.word_wrap_on,
            "auto_save_on": self.notepad.file_manager.is_auto_save_enabled,
            "auto_save_delay": self.notepad.file_manager.auto_save_delay
        }
        self.saved_preferences = preferences
        with open(self.preferences_file_path, "w") as f:
            json.dump(preferences, f, indent=4)

    def load_preferences(self) -> None:
        if os.path.exists(self.preferences_file_path):
            with open(self.preferences_file_path, "r") as f:
                preferences = json.load(f)
                self.saved_preferences = preferences
                word_wrap = self.saved_preferences.get("word_wrap_on", False)
                if word_wrap:
                    self.notepad.text.config(wrap=tkinter.WORD)
                else:
                    self.notepad.text.config(wrap=tkinter.NONE)
                auto_save = self.saved_preferences.get("auto_save_on", False)
                if auto_save:
                    self.notepad.file_manager.is_auto_save_enabled = True
                    self.notepad.file_manager.auto_save_delay = self.saved_preferences.get("auto_save_delay")
                    self.notepad.file_manager.auto_save()
                else:
                    self.notepad.file_manager.is_auto_save_enabled = False
                saved_font = tkinter.font.Font()
                saved_font.config(family=preferences.get("font_family", "Consolas"),
                                  size=preferences.get("font_size", 16),
                                  weight=preferences.get("font_weight", "normal"),
                                  slant=preferences.get("font_slant", "roman"))
                self.notepad.text.config(bg=preferences.get("background_color", "black"),
                                 fg=preferences.get("font_color", "green"),
                                 font=saved_font,
                                 selectbackground=preferences.get("selection_background_color", "#FFFF00"),
                                 selectforeground=preferences.get("selection_foreground_color", "#000000"))

    def set_preferences_to_default(self) -> None:
        current_font = tkinter.font.Font(font=self.notepad.text["font"])
        if current_font["family"] != "DejaVu Sans Mono" or current_font["size"] != 16 or current_font["weight"] != "normal" or current_font["slant"] != "roman" or self.notepad.text["bg"] != "black" or self.notepad.text["fg"] != "green" or self.word_wrap_on:
            if tkinter.messagebox.askyesno(title="Resetting Preferences", 
                                        message="Are you sure you want to reset your preferences?"):
                self.notepad.text.config(bg="black",
                                fg="green",
                                font=("DejaVu Sans Mono", 16),
                                wrap=tkinter.NONE,
                                selectbackground="#FFFF00",
                                selectforeground="#000000")
                self.notepad.file_manager.is_auto_save_enabled = False
    
    def change_font_style(self, new_font_style: str) -> None:
        new_font = tkinter.font.Font(font=self.notepad.text["font"])
        new_font = new_font.copy()
        if new_font_style == "normal" or new_font_style == "bold":
            new_font.config(weight=new_font_style)
        elif new_font_style == "roman" or new_font_style =="italic":
            new_font.config(slant=new_font_style)
        self.notepad.text.config(font=new_font)

    def change_font_size(self) -> None:
        def set_font_size(is_canceled: bool):
            if not is_canceled:
                new_font = tkinter.font.Font(font=self.notepad.text["font"])
                new_font = new_font.copy()
                new_font.config(size=scale.get())
                self.notepad.text.config(font=new_font)
            scale.destroy()
            submit_button.destroy()
            cancel_button.destroy()
            new_window.destroy()
        new_window = tkinter.Toplevel(self.notepad.window)
        new_window.geometry("200x350")
        new_window.resizable(False, False)
        new_window.title("Change Font Size")
        frame = tkinter.Frame(new_window)
        scale = tkinter.Scale(frame,
                              from_=200,
                              to=1,
                              length=250,
                              font=self.notepad.main_font)
        current_font = tkinter.font.Font(font=self.notepad.text["font"])
        scale.set(current_font["size"])
        scale.pack(expand=True, fill=tkinter.BOTH)
        submit_button = tkinter.Button(frame,
                                       text="Submit",
                                       command=lambda: set_font_size(False),
                                       font=self.notepad.main_font)
        submit_button.pack(side=tkinter.TOP, pady=5)
        cancel_button = tkinter.Button(frame,
                                       text="Cancel",
                                       command=lambda: set_font_size(True),
                                       font=self.notepad.main_font)
        cancel_button.pack(side=tkinter.TOP)
        frame.pack(expand=True)

    def load_themes(self) -> None:
        if os.path.exists(self.themes_file_path):
            with open(self.themes_file_path, "r") as f:
                self.themes = json.load(f)

    def save_themes(self) -> None:
        with open(self.themes_file_path, "w") as f:
            json.dump(self.themes, f, indent=4)

    def change_font_family(self) -> None:
        def change_font_family_execute(new_font_family_index: tuple):
            if not new_font_family_index:
                tkinter.messagebox.showwarning(title="Selection Error", message="No font family selected")
                return
            new_font = tkinter.font.Font(font=self.notepad.text["font"])
            new_font = new_font.copy()
            new_font["family"] = font_family_listbox.get(new_font_family_index[0])
            self.notepad.text.config(font=new_font)
        def change_font_family_exit():
            change_font_family_window.destroy()
        change_font_family_window = tkinter.Toplevel()
        change_font_family_window.title("Change Font Family")
        change_font_family_window.resizable(False, False)
        font_family_scrollbar = tkinter.Scrollbar(change_font_family_window,
                                                  orient=tkinter.VERTICAL)
        font_family_listbox = tkinter.Listbox(change_font_family_window,
                                              font=self.notepad.main_font,
                                              width=30,
                                              yscrollcommand=font_family_scrollbar.set)
        font_family_scrollbar.grid(row=0, column=1, rowspan=2, sticky=tkinter.NS)
        font_family_scrollbar.config(command=font_family_listbox.yview)
        font_family_listbox.grid(row=0, column=0)
        font_family_listbox.insert(0, "DejaVu Sans Mono (Default)")
        font_family_listbox.insert(1, "DejaVu Sans")
        font_family_listbox.insert(2, "DejaVu Serif")
        font_family_listbox.insert(3, "Ubuntu")
        font_family_listbox.insert(4, "Ubuntu Mono")
        font_family_listbox.insert(5, "Ubuntu Condensed")
        font_family_listbox.insert(6, "Liberation Sans")
        font_family_listbox.insert(7, "Liberation Serif")
        font_family_listbox.insert(8, "Liberation Mono")
        font_family_listbox.insert(9, "FreeSans")
        font_family_listbox.insert(10, "FreeSerif")
        font_family_listbox.insert(11, "FreeMono")
        change_font_family_buttons_frame = tkinter.Frame(change_font_family_window)
        select_font_family_button = tkinter.Button(change_font_family_buttons_frame,
                                                   font=self.notepad.main_font,
                                                   text="Select",
                                                   command=lambda: change_font_family_execute(font_family_listbox.curselection()))
        select_font_family_button.pack(side=tkinter.LEFT)
        exit_font_family_button = tkinter.Button(change_font_family_buttons_frame,
                                                 font=self.notepad.main_font,
                                                 text="Exit",
                                                 command=change_font_family_exit)
        exit_font_family_button.pack(side=tkinter.LEFT)
        change_font_family_buttons_frame.grid(row=1, column=0, columnspan=2)

    def manage_themes(self) -> None:
        def add_new_theme():
            def set_background_color() -> None:
                background_color = tkinter.colorchooser.askcolor(title="Background Color")[1]
                background_color_canvas.create_rectangle(0, 0, 36, 36, fill=background_color)
                background_color_canvas.config(highlightbackground=background_color, bd=0, highlightthickness=1)
                bg_color.set(background_color)

            def set_foreground_color() -> None:
                foreground_color = tkinter.colorchooser.askcolor(title="Font Color")[1]
                foreground_color_canvas.create_rectangle(0, 0, 36, 36, fill=foreground_color)
                foreground_color_canvas.config(highlightbackground=foreground_color, bd=0, highlightthickness=1)
                fg_color.set(foreground_color)

            def set_selection_background_color() -> None:
                selection_background_color = tkinter.colorchooser.askcolor(title="Selection Background Color")[1]
                selection_background_color_canvas.create_rectangle(0, 0, 36, 36, fill=selection_background_color)
                selection_background_color_canvas.config(highlightbackground=selection_background_color, bd=0, highlightthickness=1)
                selection_bg_color.set(selection_background_color)

            def set_selection_foreground_color() -> None:
                selection_foreground_color = tkinter.colorchooser.askcolor(title="Selection Font Color")[1]
                selection_foreground_color_canvas.create_rectangle(0, 0, 36, 36, fill=selection_foreground_color)
                selection_foreground_color_canvas.config(highlightbackground=selection_foreground_color, bd=0, highlightthickness=1)
                selection_fg_color.set(selection_foreground_color)

            def save():
                theme_name.set(theme_name_entry.get())
                if not theme_name.get():
                    tkinter.messagebox.showwarning(title="No theme name", message="Please, enter the theme name")
                    return
                if not bg_color.get():
                    tkinter.messagebox.showwarning(title="No background color", message="Please, select the background color")
                    return
                if not fg_color.get():
                    tkinter.messagebox.showwarning(title="No font color", message="Please, select the font color")
                    return
                if not selection_bg_color.get():
                    tkinter.messagebox.showwarning(title="Selection Error", message="No selection background color selected")
                    return
                if not selection_fg_color.get():
                    tkinter.messagebox.showwarning(title="Selection Error", message="No selection foreground color selected")
                    return
                new_theme = {
                    "theme_name": theme_name.get(),
                    "background_color": bg_color.get(),
                    "foreground_color": fg_color.get(),
                    "selection_background_color": selection_bg_color.get(),
                    "selection_foreground_color": selection_fg_color.get()
                }
                self.themes.append(new_theme)
                self.save_themes()
                refresh_themes()
                add_theme_window.destroy()

            def cancel():
                add_theme_window.destroy()

            add_theme_window = tkinter.Toplevel(new_window)
            main_frame = tkinter.Frame(add_theme_window)
            add_theme_window.resizable(False, False)
            add_theme_window.title("Add New Theme")
            theme_name = tkinter.StringVar()
            bg_color = tkinter.StringVar()
            fg_color = tkinter.StringVar()
            selection_bg_color = tkinter.StringVar()
            selection_fg_color = tkinter.StringVar()
            name_frame = tkinter.Frame(main_frame)
            name_label = tkinter.Label(name_frame,
                                       text="Name: ",
                                       font=self.notepad.main_font)
            name_label.pack(side=tkinter.LEFT)
            theme_name_entry = tkinter.Entry(name_frame,
                                             font=self.notepad.main_font)
            theme_name_entry.pack(side=tkinter.LEFT)
            name_frame.pack(side=tkinter.TOP,
                            pady=5)
            background_color_frame = tkinter.Frame(main_frame)
            background_color_canvas = tkinter.Canvas(background_color_frame,
                                            width=36,
                                            height=36,
                                            bd=1,
                                            relief=tkinter.RAISED)
            background_color_canvas.pack(side=tkinter.LEFT)
            background_color_button = tkinter.Button(background_color_frame,
                                                     text="Set Background Color",
                                                     command=set_background_color,
                                                     font=self.notepad.main_font,
                                                     width=31)
            background_color_button.pack(side=tkinter.LEFT)
            background_color_frame.pack(side=tkinter.TOP,
                                        pady=5)
            foreground_color_frame = tkinter.Frame(main_frame)
            foreground_color_canvas = tkinter.Canvas(foreground_color_frame,
                                            width=36,
                                            height=36,
                                            bd=1,
                                            relief=tkinter.RAISED)
            foreground_color_canvas.pack(side=tkinter.LEFT)
            foreground_color_button = tkinter.Button(foreground_color_frame,
                                                     text="Set Font Color",
                                                     command=set_foreground_color,
                                                     font=self.notepad.main_font,
                                                     width=31)
            foreground_color_button.pack(side=tkinter.LEFT)
            foreground_color_frame.pack(side=tkinter.TOP,
                                        pady=5)
            selection_background_color_frame = tkinter.Frame(main_frame)
            selection_background_color_canvas = tkinter.Canvas(selection_background_color_frame,
                                                    width=36,
                                                    height=36,
                                                    bd=1,
                                                    relief=tkinter.RAISED)
            selection_background_color_canvas.pack(side=tkinter.LEFT)
            selection_background_color_button = tkinter.Button(selection_background_color_frame,
                                                     text="Selection Background Color",
                                                     command=set_selection_background_color,
                                                     font=self.notepad.main_font,
                                                     width=31)
            selection_background_color_button.pack(side=tkinter.LEFT)
            selection_background_color_frame.pack(side=tkinter.TOP,
                                        pady=5)
            selection_foreground_color_frame = tkinter.Frame(main_frame)
            selection_foreground_color_canvas = tkinter.Canvas(selection_foreground_color_frame,
                                                    width=36,
                                                    height=36,
                                                    bd=1,
                                                    relief=tkinter.RAISED)
            selection_foreground_color_canvas.pack(side=tkinter.LEFT)
            selection_foreground_color_button = tkinter.Button(selection_foreground_color_frame,
                                                     text="Selection Font Color",
                                                     command=set_selection_foreground_color,
                                                     font=self.notepad.main_font,
                                                     width=31)
            selection_foreground_color_button.pack(side=tkinter.LEFT)
            selection_foreground_color_frame.pack(side=tkinter.TOP,
                                        pady=5)
            button_frame = tkinter.Frame(main_frame)
            save_button = tkinter.Button(button_frame,
                                         font=self.notepad.main_font,
                                         text="Save",
                                         command=save)
            save_button.pack(side=tkinter.LEFT)
            cancel_button = tkinter.Button(button_frame,
                                           font=self.notepad.main_font,
                                           text="Cancel",
                                           command=cancel)
            save_button.pack(side=tkinter.LEFT)
            cancel_button.pack(side=tkinter.LEFT)
            button_frame.pack(side=tkinter.TOP,
                              pady=5)
            main_frame.pack(expand=True)

        def change_theme(theme_id: tuple) -> None:
            if not theme_id:
                tkinter.messagebox.showwarning(title="Selection Error", message="No option selected")
                return
            for (index, theme) in zip(range(len(self.themes)), self.themes):
                if theme_id[0] == index:
                    self.notepad.text.config(bg=theme["background_color"],
                                             fg=theme["foreground_color"],
                                             selectbackground=theme["selection_background_color"],
                                             selectforeground=theme["selection_foreground_color"])
                    return
            add_new_theme()

        def delete_theme(theme_id: tuple) -> None:
            if not theme_id:
                tkinter.messagebox.showwarning(title="Selection Error", message="No option selected")
                return
            if theme_id[0] in range(self.default_themes_count):
                tkinter.messagebox.showwarning(title="Permission Denied", message="You can't delete a default theme")
                return
            if theme_id[0] == themes_listbox.size() - 1:
                tkinter.messagebox.showwarning(title="Selection Error", message="Invalid choice")
                return
            index = theme_id[0]
            for i in range(len(self.themes)):
                if index == i:
                    if tkinter.messagebox.askyesno(title="Deleting Theme", 
                                                   message=f'Are you sure you want to delete "{self.themes[index]["theme_name"]}"'):
                        self.themes.pop(index)
                        themes_listbox.delete(index)
                        self.save_themes()
                        refresh_themes()
                        break
                    else:
                        break
        def end():
            themes_listbox.destroy()
            select_button.destroy()
            new_window.destroy()

        def refresh_themes():
            themes_listbox.delete(0, tkinter.END)
            for theme in self.themes:
                themes_listbox.insert(tkinter.END, theme["theme_name"])
            themes_listbox.insert(tkinter.END, "[ADD NEW THEME]")
            for (index, theme) in zip(range(len(self.themes)), self.themes):
                themes_listbox.itemconfig(index,
                                        bg=theme["background_color"],
                                        fg=theme["foreground_color"])
                themes_listbox.itemconfig(tkinter.END,
                                    bg="#27ae60",
                                    fg="white")
        new_window = tkinter.Toplevel(self.notepad.window)
        new_window.resizable(False, False)
        frame = tkinter.Frame(new_window)
        new_window.title("Themes")
        themes_listbox_scrollbar = tkinter.Scrollbar(new_window,
                                                     orient=tkinter.VERTICAL)
        themes_listbox = tkinter.Listbox(frame, font=self.notepad.main_font, yscrollcommand=themes_listbox_scrollbar.set)
        themes_listbox_scrollbar.config(command=themes_listbox.yview)
        themes_listbox.pack()
        themes_listbox_scrollbar.pack(side=tkinter.RIGHT,
                                      fill=tkinter.Y)
        for theme in self.themes:
            themes_listbox.insert(tkinter.END, theme["theme_name"])
        themes_listbox.insert(tkinter.END, "[ADD NEW THEME]")
        for (index, theme) in zip(range(themes_listbox.size()), self.themes):
            themes_listbox.itemconfig(index, bg=theme["background_color"], fg=theme["foreground_color"])
        themes_listbox.itemconfig(tkinter.END,
                                  bg="#27ae60",
                                  fg="white",
                                  selectbackground="red",
                                  selectforeground="white")
        buttons_frame = tkinter.Frame(frame)
        select_button = tkinter.Button(buttons_frame,
                                       text="Select",
                                       font=self.notepad.main_font,
                                       command=lambda: change_theme(themes_listbox.curselection()))
        select_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        delete_button = tkinter.Button(buttons_frame,
                                        text="Delete",
                                        font=self.notepad.main_font,
                                        command=lambda: delete_theme(themes_listbox.curselection()))
        delete_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        exit_button = tkinter.Button(buttons_frame,
                                     text="Exit",
                                     font=self.notepad.main_font,
                                     command=end)
        exit_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        buttons_frame.pack()
        frame.pack(expand=True)