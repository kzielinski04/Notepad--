import tkinter
import tkinter.scrolledtext
import tkinter.filedialog
import tkinter.colorchooser
import tkinter.font
import tkinter.messagebox
import os
import json
import random

class Icons:
    def __init__(self):
        self.new_file_icon = tkinter.PhotoImage(file="new_file_icon.png")
        self.open_file_icon = tkinter.PhotoImage(file="open_file_icon.png")
        self.save_file_icon = tkinter.PhotoImage(file="save_file_icon.png")
        self.app_icon = tkinter.PhotoImage(file="app_icon.png")
        self.exit_icon = tkinter.PhotoImage(file="exit_icon.png")
        self.change_font_family_icon = tkinter.PhotoImage(file="change_font_family_icon.png")
        self.clear_icon = tkinter.PhotoImage(file="clear_icon.png")
        self.reset_icon = tkinter.PhotoImage(file="reset_icon.png")
        self.change_background_color_icon = tkinter.PhotoImage(file="change_background_color_icon.png")
        self.change_font_color_icon = tkinter.PhotoImage(file="change_font_color_icon.png")
        self.change_font_size_icon = tkinter.PhotoImage(file="change_font_size_icon.png")
        self.change_font_style_icon = tkinter.PhotoImage(file="change_font_style_icon.png")
        self.find_and_replace_icon = tkinter.PhotoImage(file="find_and_replace_icon.png")
        self.generate_random_text_icon = tkinter.PhotoImage(file="generate_random_text_icon.png")
        self.themes_icon = tkinter.PhotoImage(file="themes_icon.png")
        self.word_wrap_icon = tkinter.PhotoImage(file="word_wrap_icon.png")
        self.find_icon = tkinter.PhotoImage(file="find_icon.png")
        self.cut_icon = tkinter.PhotoImage(file="cut_icon.png")
        self.copy_icon = tkinter.PhotoImage(file="copy_icon.png")
        self.paste_icon = tkinter.PhotoImage(file="paste_icon.png")
        self.undo_icon = tkinter.PhotoImage(file="undo_icon.png")
        self.redo_icon = tkinter.PhotoImage(file="redo_icon.png")

class Notepad:
    def __init__(self):
        self.preferences_file_path = "preferences.json"
        self.themes_file_path = "themes.json"
        self.saved_content = ""
        self.saved_preferences = {}
        self.word_wrap_on = False
        self.saved_file_path = ""
        self.themes = []
        self.characters_count = 0
        self.words_count = 0
        self.default_themes_count = 9
        self.window = tkinter.Tk()
        self.counters_frame = tkinter.Frame(self.window)
        self.main_frame = tkinter.Frame(self.window)
        self.main_font = tkinter.font.Font(family="DejaVu Sans Mono",
                                           size=16)
        self.text = tkinter.scrolledtext.ScrolledText(self.main_frame,
                                                      font=self.main_font,
                                                      undo=True,
                                                      autoseparators=True)
        self.characters_count_label = tkinter.Label(self.counters_frame,
                                                      font=self.main_font,
                                                      text=f"Characters Count: {self.characters_count}")
        self.words_count_label = tkinter.Label(self.counters_frame,
                                               font=self.main_font,
                                               text=f"Words Count: {self.words_count}")
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

    def new_file(self, event=None) -> None:
        file_content = self.text.get(1.0, tkinter.END)
        if (len(file_content) - 1) != 0 and file_content != self.saved_content:
            choice = tkinter.messagebox.askyesno(message="Do you want to save your file before creating a new one?")
            if choice:
                self.save_file_as()
        self.clear_file()

    def open_file(self, event=None) -> None:
        file_content = self.text.get(1.0, tkinter.END)
        if (len(file_content) - 1) != 0 and file_content != self.saved_content:
            choice = tkinter.messagebox.askyesno(message="Do you want to save your file before opening a new one?")
            if choice:
                self.save_file_as()
            else:
                return
        file_path = tkinter.filedialog.askopenfilename(initialdir="/~/Desktop",
                                                       filetypes=[("Text files", "*.txt"),
                                                                  ("HTML files", "*.html"),
                                                                  ("CSV files", "*.csv"),
                                                                  ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as f:
                content = f.read()
                self.clear_file()
                self.text.insert(1.0, content)

    def save_file(self, event=None) -> None:
        if not self.saved_file_path:
            self.save_file_as()
        else:
            with open(self.saved_file_path, "w") as f:
                content = self.text.get(1.0, tkinter.END)
                f.write(content)
                self.saved_content = content

    def save_file_as(self, event=None) -> None:
        self.file_path = tkinter.filedialog.asksaveasfilename(initialdir="/~/Desktop",
                                                              defaultextension=".txt",
                                                              filetypes=[("Text files", "*.txt"),
                                                                         ("HTML files", "*.html"),
                                                                         ("CSV files", "*.csv"),
                                                                         ("All files", "*.*")])
        if not self.file_path:
            return
        self.saved_file_path = self.file_path
        with open(self.file_path, "w") as f:
            content = self.text.get(1.0, tkinter.END)
            f.write(content)
            self.saved_content = content

    def exit(self) -> None:
        content = self.text.get(1.0, tkinter.END)
        if (len(content) - 1) != 0 and content != self.saved_content:
            choice = tkinter.messagebox.askyesno(message="Do you want to save your file before exit?")
            if choice:
                if not self.saved_file_path:
                    self.save_file_as()
                else:
                    self.save_file()
        current_font = tkinter.font.Font(font=self.text["font"])
        current_preferences = {
            "background_color": self.text["bg"],
            "font_color": self.text["fg"],
            "font_family": current_font["family"],
            "font_weight": current_font["weight"],
            "font_slant": current_font["slant"],
            "font_size": current_font["size"],
            "word_wrap_on": self.word_wrap_on
        }
        for (cp, sp) in zip(current_preferences.values(), self.saved_preferences.values()):
            if cp != sp:
                choice = tkinter.messagebox.askyesno(message="Do you want to save your preferences before exit?")
                if choice:
                    self.save_preferences()
                break        
        self.window.quit()

    def change_background_color(self) -> None:
        color = tkinter.colorchooser.askcolor(title="Change Background Color")[1]
        self.text.config(bg=color)

    def change_font_color(self) -> None:
        color = tkinter.colorchooser.askcolor(title="Change Font Color")[1]
        self.text.config(fg=color)

    def save_preferences(self) -> None:
        current_font = tkinter.font.Font(font=self.text["font"])
        background_color = self.text["bg"]
        font_color = self.text["fg"]
        font_family = current_font["family"]
        font_weight = current_font["weight"]
        font_size = current_font["size"]
        font_weight = current_font["weight"]
        font_slant = current_font["slant"]
        preferences = {
            "background_color": background_color,
            "font_color": font_color,
            "font_family": font_family,
            "font_weight": font_weight,
            "font_slant": font_slant,
            "font_size": font_size,
            "word_wrap_on": self.word_wrap_on
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
                    self.text.config(wrap=tkinter.WORD)
                else:
                    self.text.config(wrap=tkinter.NONE)
                saved_font = tkinter.font.Font()
                saved_font.config(family=preferences.get("font_family", "Consolas"),
                                  size=preferences.get("font_size", 16),
                                  weight=preferences.get("font_weight", "normal"),
                                  slant=preferences.get("font_slant", "roman"))
                self.text.config(bg=preferences.get("background_color", "black"),
                                 fg=preferences.get("font_color", "green"),
                                 font=saved_font)

    def set_preferences_to_default(self) -> None:
        current_font = tkinter.font.Font(font=self.text["font"])
        if current_font["family"] != "DejaVu Sans Mono" or current_font["size"] != 16 or current_font["weight"] != "normal" or current_font["slant"] != "roman" or self.text["bg"] != "black" or self.text["fg"] != "green" or self.word_wrap_on:
            if tkinter.messagebox.askyesno(title="Resetting Preferences", 
                                        message="Are you sure you want to reset your preferences?"):
                self.text.config(bg="black",
                                fg="green",
                                font=("DejaVu Sans Mono", 16),
                                wrap=tkinter.NONE)

    def change_font_family(self) -> None:
        def change_font_family_execute(new_font_family_index: tuple):
            if not new_font_family_index:
                tkinter.messagebox.showwarning(title="Selection Error", message="No font family selected")
                return
            new_font = tkinter.font.Font(font=self.text["font"])
            new_font = new_font.copy()
            new_font["family"] = font_family_listbox.get(new_font_family_index[0])
            self.text.config(font=new_font)
        def change_font_family_exit():
            change_font_family_window.destroy()
        change_font_family_window = tkinter.Toplevel()
        change_font_family_window.title("Change Font Family")
        change_font_family_window.resizable(False, False)
        font_family_scrollbar = tkinter.Scrollbar(change_font_family_window,
                                                  orient=tkinter.VERTICAL)
        font_family_listbox = tkinter.Listbox(change_font_family_window,
                                              font=self.main_font,
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
                                                   font=self.main_font,
                                                   text="Select",
                                                   command=lambda: change_font_family_execute(font_family_listbox.curselection()))
        select_font_family_button.pack(side=tkinter.LEFT)
        exit_font_family_button = tkinter.Button(change_font_family_buttons_frame,
                                                 font=self.main_font,
                                                 text="Exit",
                                                 command=change_font_family_exit)
        exit_font_family_button.pack(side=tkinter.LEFT)
        change_font_family_buttons_frame.grid(row=1, column=0, columnspan=2)

    def change_font_style(self, new_font_style: str) -> None:
        new_font = tkinter.font.Font(font=self.text["font"])
        new_font = new_font.copy()
        if new_font_style == "normal" or new_font_style == "bold":
            new_font.config(weight=new_font_style)
        elif new_font_style == "roman" or new_font_style =="italic":
            new_font.config(slant=new_font_style)
        self.text.config(font=new_font)

    def change_font_size(self) -> None:
        def set_font_size(is_canceled: bool):
            if not is_canceled:
                new_font = tkinter.font.Font(font=self.text["font"])
                new_font = new_font.copy()
                new_font.config(size=scale.get())
                self.text.config(font=new_font)
            scale.destroy()
            submit_button.destroy()
            cancel_button.destroy()
            new_window.destroy()
        new_window = tkinter.Toplevel(self.window)
        new_window.geometry("500x350")
        new_window.resizable(False, False)
        new_window.title("Change Font Size")
        frame = tkinter.Frame(new_window)
        scale = tkinter.Scale(frame,
                              from_=100,
                              to=1,
                              length=250,
                              font=self.main_font)
        current_font = tkinter.font.Font(font=self.text["font"])
        scale.set(current_font["size"])
        scale.pack(side=tkinter.TOP)
        submit_button = tkinter.Button(frame,
                                       text="Submit",
                                       command=lambda: set_font_size(False),
                                       font=self.main_font)
        submit_button.pack(side=tkinter.TOP)
        cancel_button = tkinter.Button(frame,
                                       text="Cancel",
                                       command=lambda: set_font_size(True),
                                       font=self.main_font)
        cancel_button.pack(side=tkinter.TOP)
        frame.pack(expand=True)

    def load_themes(self) -> None:
        if os.path.exists(self.themes_file_path):
            with open(self.themes_file_path, "r") as f:
                self.themes = json.load(f)

    def save_themes(self) -> None:
        with open(self.themes_file_path, "w") as f:
            json.dump(self.themes, f, indent=4)

    def manage_themes(self) -> None:
        def add_new_theme():
            def set_background_color() -> None:
                background_color = tkinter.colorchooser.askcolor(title="Background Color")[1]
                background_color_label.config(bg=background_color)
                bg_color.set(background_color)
            def set_foreground_color() -> None:
                foreground_color = tkinter.colorchooser.askcolor(title="Font Color")[1]
                foreground_color_label.config(bg=foreground_color)
                fg_color.set(foreground_color)
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
                new_theme = {
                    "theme_name": theme_name.get(),
                    "background_color": bg_color.get(),
                    "foreground_color": fg_color.get()
                }
                self.themes.append(new_theme)
                self.save_themes()
                refresh_themes()
                add_theme_window.destroy()
            def cancel():
                add_theme_window.destroy()
            add_theme_window = tkinter.Toplevel(new_window)
            main_frame = tkinter.Frame(add_theme_window)
            add_theme_window.geometry("350x250")
            add_theme_window.resizable(False, False)
            add_theme_window.title("Add New Theme")
            theme_name = tkinter.StringVar()
            bg_color = tkinter.StringVar()
            fg_color = tkinter.StringVar()
            name_frame = tkinter.Frame(main_frame)
            name_label = tkinter.Label(name_frame,
                                       text="Name: ",
                                       font=self.main_font)
            name_label.pack(side=tkinter.LEFT)
            theme_name_entry = tkinter.Entry(name_frame,
                                             font=self.main_font)
            theme_name_entry.pack(side=tkinter.LEFT)
            name_frame.pack(side=tkinter.TOP,
                            pady=5)
            background_color_frame = tkinter.Frame(main_frame)
            background_color_label = tkinter.Label(background_color_frame,
                                            width=5,
                                            height=2,
                                            bd=5,
                                            relief=tkinter.RAISED)
            background_color_label.pack(side=tkinter.LEFT)
            background_color_button = tkinter.Button(background_color_frame,
                                                     text="Set background color",
                                                     command=set_background_color,
                                                     font=self.main_font,
                                                     width=31)
            background_color_button.pack(side=tkinter.LEFT)
            background_color_frame.pack(side=tkinter.TOP,
                                        pady=5)
            foreground_color_frame = tkinter.Frame(main_frame)
            foreground_color_label = tkinter.Label(foreground_color_frame,
                                            width=5,
                                            height=2,
                                            bd=5,
                                            relief=tkinter.RAISED)
            foreground_color_label.pack(side=tkinter.LEFT)
            foreground_color_button = tkinter.Button(foreground_color_frame,
                                                     text="Set font color",
                                                     command=set_foreground_color,
                                                     font=self.main_font,
                                                     width=31)
            foreground_color_button.pack(side=tkinter.LEFT)
            foreground_color_frame.pack(side=tkinter.TOP,
                                        pady=5)
            button_frame = tkinter.Frame(main_frame)
            save_button = tkinter.Button(button_frame,
                                         font=self.main_font,
                                         text="Save",
                                         command=save)
            save_button.pack(side=tkinter.LEFT)
            cancel_button = tkinter.Button(button_frame,
                                           font=self.main_font,
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
                    self.text.config(bg=theme["background_color"],
                                     fg=theme["foreground_color"])
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
        new_window = tkinter.Toplevel(self.window)
        new_window.resizable(False, False)
        frame = tkinter.Frame(new_window)
        new_window.title("Themes")
        themes_listbox_scrollbar = tkinter.Scrollbar(new_window,
                                                     orient=tkinter.VERTICAL)
        themes_listbox = tkinter.Listbox(frame, font=self.main_font, yscrollcommand=themes_listbox_scrollbar.set)
        themes_listbox_scrollbar.config(command=themes_listbox.yview)
        themes_listbox.pack()
        themes_listbox_scrollbar.pack(side=tkinter.RIGHT,
                                      fill=tkinter.Y)
        for theme in self.themes:
            themes_listbox.insert(tkinter.END, theme["theme_name"])
        themes_listbox.insert(tkinter.END, "[ADD NEW THEME]")
        for (index, theme) in zip(range(themes_listbox.size()), self.themes):
            themes_listbox.itemconfig(index,
                                    bg=theme["background_color"],
                                    fg=theme["foreground_color"])
        themes_listbox.itemconfig(tkinter.END,
                                  bg="#27ae60",
                                  fg="white",
                                  selectbackground="red",
                                  selectforeground="white"
                                  )
        buttons_frame = tkinter.Frame(frame)
        select_button = tkinter.Button(buttons_frame,
                                       text="Select",
                                       font=self.main_font,
                                       command=lambda: change_theme(themes_listbox.curselection()))
        select_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        delete_button = tkinter.Button(buttons_frame,
                                        text="Delete",
                                        font=self.main_font,
                                        command=lambda: delete_theme(themes_listbox.curselection()))
        delete_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        exit_button = tkinter.Button(buttons_frame,
                                     text="Exit",
                                     font=self.main_font,
                                     command=end)
        exit_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        buttons_frame.pack()
        frame.pack(expand=True)

    def clear_file(self, event=None) -> None:
        """Clears file with confirmation"""
        if self.text_is_empty():
            tkinter.messagebox.showwarning(title="Empty File", message="This file is empty")
            return
        if tkinter.messagebox.askyesno(title="Clearing Document", message="Are you sure you want to clear this file?"):
            self.text.delete(1.0, tkinter.END)
        else:
            return

    def clear_text(self, event=None) -> None:
        """Clears file without confirmation"""
        self.text.delete(1.0, tkinter.END)

    def text_is_empty(self) -> bool:
        return len(self.text.get(1.0, tkinter.END)) - 1 == 0

    def find(self, event=None) -> None:
        matches = []
        current_selection_start_index = tkinter.StringVar()
        current_selection_end_index = tkinter.StringVar()
        current_selection_matches_index = tkinter.IntVar()
        is_executed = tkinter.BooleanVar(value=False)
        def find_execute(event=None):
            if not find_entry.get():
                tkinter.messagebox.showwarning(title="Empty Input",
                                               message="Find text can't be empty")
                is_executed.set(False)
                return
            is_executed.set(True)
            try:
                self.text.tag_remove(tkinter.SEL, tkinter.SEL_FIRST, tkinter.SEL_LAST)
            except Exception:
                pass
            if matches:
                for m in enumerate(matches):
                    self.text.tag_remove("match_found", m[1][0], m[1][1])
            matches.clear()

            def next_match(event=None):
                if matches:
                    current_selection_start_index.set(self.text.index(tkinter.SEL_FIRST))
                    current_selection_end_index.set(self.text.index(tkinter.SEL_LAST))
                    for i, m in enumerate(matches):
                        if m[0] == current_selection_start_index.get():
                            current_selection_matches_index.set(i)
                            break
                    if current_selection_matches_index.get() == len(matches) - 1:
                        current_selection_matches_index.set(0)
                        match_count_label.config(text=f"{current_selection_matches_index.get() + 1}/{match_count}")
                        new_selection_start_index = matches[0][0]
                        new_selection_end_index = matches[0][1]
                    else:
                        current_selection_matches_index.set(current_selection_matches_index.get() + 1)
                        match_count_label.config(text=f"{current_selection_matches_index.get() + 1}/{match_count}")
                        new_selection_start_index = matches[current_selection_matches_index.get()][0]
                        new_selection_end_index = matches[current_selection_matches_index.get()][1]
                    self.text.tag_remove(tkinter.SEL, current_selection_start_index.get(), current_selection_end_index.get())
                    self.text.tag_add(tkinter.SEL, new_selection_start_index, new_selection_end_index)
                    current_selection_start_index.set(new_selection_start_index)
                    current_selection_end_index.set(new_selection_end_index)

            def previous_match(event=None):
                if matches:
                    current_selection_start_index.set(self.text.index(tkinter.SEL_FIRST))
                    current_selection_end_index.set(self.text.index(tkinter.SEL_LAST))
                    for i, m in enumerate(matches):
                        if m[0] == current_selection_start_index.get():
                            current_selection_matches_index.set(i)
                            break
                    if current_selection_matches_index.get() == 0:
                        current_selection_matches_index.set(len(matches) - 1)
                        match_count_label.config(text=f"{current_selection_matches_index.get() + 1}/{match_count}")
                        new_selection_start_index = matches[len(matches) - 1][0]
                        new_selection_end_index = matches[len(matches) - 1][1]
                    else:
                        current_selection_matches_index.set(current_selection_matches_index.get() - 1)
                        match_count_label.config(text=f"{current_selection_matches_index.get() + 1}/{match_count}")
                        new_selection_start_index = matches[current_selection_matches_index.get()][0]
                        new_selection_end_index = matches[current_selection_matches_index.get()][1]
                    self.text.tag_remove(tkinter.SEL, current_selection_start_index.get(), current_selection_end_index.get())
                    self.text.tag_add(tkinter.SEL, new_selection_start_index, new_selection_end_index)
                    current_selection_start_index.set(new_selection_start_index)
                    current_selection_end_index.set(new_selection_end_index)

            find_previous_button = tkinter.Button(find_frame,
                                          font=self.main_font,
                                          text="<-",
                                          command=previous_match)
            find_previous_button.grid(row=1, column=0)
            find_button.grid(row=1, column=1)
            find_next_button = tkinter.Button(find_frame,
                                          font=self.main_font,
                                          text="->",
                                          command=next_match)
            find_next_button.grid(row=1, column=2)
            if is_executed:
                find_window.bind("<Left>", previous_match)
                find_window.bind("<Right>", next_match)
            find_text = find_entry.get()
            start_index = "1.0"
            match_count = 0
            while True:
                text_match_index = self.text.search(find_text, start_index, tkinter.END)
                if not text_match_index:
                    break
                match_count += 1
                self.text.tag_add("match_found",
                                text_match_index,
                                f"{text_match_index}+{len(find_text)}c")
                self.text.tag_config("match_found", background="yellow")
                current_match = (text_match_index, f"{text_match_index}+{len(find_text)}c")
                matches.append(current_match)
                start_index = f"{text_match_index}+{len(find_text)}c"
            if match_count != 0:
                self.text.tag_add(tkinter.SEL, matches[0][0], matches[0][1])
                current_selection_start_index.set(self.text.index(tkinter.SEL_FIRST))
                current_selection_end_index.set(self.text.index(tkinter.SEL_LAST))
                match_count_label = tkinter.Label(find_window,
                                                font=self.main_font,
                                                text=f"1/{match_count}")
            else:
                match_count_label = tkinter.Label(find_window,
                                                font=self.main_font,
                                                text="0/0")
            match_count_label.grid(row=2, column=0, columnspan=3)
            
        def find_exit():
            if matches:
                for m in matches:
                    self.text.tag_remove("match_found", m[0], m[1])
            find_window.destroy()

        find_window = tkinter.Toplevel(self.window)
        find_window.title("Find")
        find_window.resizable(False, False)
        find_window.protocol("WM_DELETE_WINDOW", find_exit)
        find_label = tkinter.Label(find_window,
                                   font=self.main_font,
                                   text="Enter the text to find: ")
        find_entry = tkinter.Entry(find_window,
                                   font=self.main_font)
        find_label.grid(row=0, column=0, pady=5)
        find_entry.grid(row=0, column=1, pady=5)
        find_frame = tkinter.Frame(find_window)
        find_button = tkinter.Button(find_frame,
                                     font=self.main_font,
                                     text="Find",
                                     command=find_execute)
        find_window.bind("<Return>", find_execute)
        find_button.grid(row=0, column=2)
        find_frame.grid(row=1, column=0, columnspan=2, pady=5)

    def find_and_replace(self, event=None) -> None:
        def execute(event=None):
            if not find_entry.get() and not replace_entry.get():
                tkinter.messagebox.showwarning(title="No Input Error",
                                               message="Find Text and Replace Text not entered")
                return
            elif not find_entry.get():
                tkinter.messagebox.showwarning(title="No Input Error",
                                               message="Find Text not entered")
                return
            elif not replace_entry.get():
                tkinter.messagebox.showwarning(title="No Input Error",
                                               message="Replace Text not entered")
                return
            content = self.text.get(1.0, tkinter.END)
            find = find_entry.get()
            replace = replace_entry.get()
            result = content.replace(find, replace)
            match_count = content.count(find)
            self.clear_text()
            self.text.insert(1.0, result)
            if match_count == 0:
                tkinter.messagebox.showinfo(title="No Matches", message="No matches found")
            else:
                tkinter.messagebox.showinfo(title="Find & Replace Completed", message=f"Replaced {match_count} occurences")
            find_and_replace_window.destroy()
        if self.text_is_empty():
            tkinter.messagebox.showwarning(title="Empty File", message="This file is empty")
            return
        find_and_replace_window = tkinter.Toplevel(self.window)
        find_and_replace_window.title("Find & Replace")
        find_and_replace_window.resizable(False, False)
        find_label = tkinter.Label(find_and_replace_window,
                                   text="Enter the text to find: ",
                                   font=self.main_font)
        find_label.grid(row=0,
                        column=0,
                        pady=5)
        find_entry = tkinter.Entry(find_and_replace_window,
                                   font=self.main_font)
        find_entry.grid(row=0,
                        column=1,
                        pady=5)
        replace_label = tkinter.Label(find_and_replace_window,
                                   text="Enter the text to replace: ",
                                   font=self.main_font)
        replace_label.grid(row=1,
                           column=0,
                           pady=5)
        replace_entry = tkinter.Entry(find_and_replace_window,
                                   font=self.main_font)
        replace_entry.grid(row=1,
                           column=1,
                           pady=5)
        submit_button = tkinter.Button(find_and_replace_window,
                                       text="Find & Replace",
                                       command=execute,
                                       font=self.main_font)
        submit_button.grid(row=2,
                           column=0,
                           columnspan=2,
                           pady=5)
        find_and_replace_window.bind("<Return>", execute)

    def generate_random_text(self, event=None) -> None:
        def generate_random_text_execute(event=None):
            content = self.text.get(1.0, tkinter.END) 
            if (len(content) - 1) != 0 and content != self.saved_content:
                choice = tkinter.messagebox.askyesno(message="Do you want to save your file before generating the random text?")
                if choice:
                    if len(self.saved_file_path) == 0:
                        self.save_file_as()
                    else:
                        self.save_file()
            length = random_text_length_entry.get()
            if not length.isdigit() or int(length) == 0:
                tkinter.messagebox.showwarning(title="Input Error", message="Length must be a positive number")
                return
            length = int(length)
            result = ""
            for i in range(length):
                result = result + chr(random.randint(32, 126))
            self.clear_text()
            self.text.insert(1.0, result)
            generate_random_text_window.destroy()

        generate_random_text_window = tkinter.Toplevel(self.window)
        generate_random_text_window.title("Generate Random Text")
        random_text_length_label = tkinter.Label(generate_random_text_window,
                                                 font=self.main_font,
                                                 text="Enter the length of the random text: ")
        random_text_length_label.grid(row=0,
                                      column=0,
                                      pady=5)
        random_text_length_entry = tkinter.Entry(generate_random_text_window,
                                                 font=self.main_font)
        random_text_length_entry.grid(row=0,
                                      column=1,
                                      pady=5)
        generate_random_text_button = tkinter.Button(generate_random_text_window,
                                                     font=self.main_font,
                                                     text="Generate",
                                                     command=generate_random_text_execute)
        generate_random_text_button.grid(row=1,
                                         column=0,
                                         columnspan=2,
                                         pady=5)
        generate_random_text_window.bind("<Return>", generate_random_text_execute)

    def count_characters_and_words(self, event=None) -> None:
        content = self.text.get(1.0, tkinter.END)
        char_counter = -1
        for c in content:
            if c != " ":
                char_counter = char_counter + 1
        self.characters_count = char_counter
        self.characters_count_label.config(text=f"Characters Count: {self.characters_count}")

        content = content.split()
        words_counter = 0
        for c in content:
            if c != " ":
                words_counter += 1
        self.words_count = words_counter
        self.words_count_label.config(text=f"Words Count: {self.words_count}")

    def toggle_word_wrap(self, event=None) -> None:
        if self.word_wrap_on:
            self.word_wrap_on = False
            self.text.config(wrap=tkinter.NONE)
            tkinter.messagebox.showinfo(title="Word Wrap OFF", message="Word Wrap is now disabled")
        else:
            self.word_wrap_on = True
            self.text.config(wrap=tkinter.WORD)
            tkinter.messagebox.showinfo(title="Word Wrap ON", message="Word Wrap is now enabled")

    def undo(self, event=None) -> None:
        try:
            self.text.edit_undo()
        except tkinter.TclError:
            tkinter.messagebox.showwarning(title="Undo Error", message="Nothing to undo")

    def redo(self, event=None) -> None:
        try:
            self.text.edit_redo()
        except tkinter.TclError:
            tkinter.messagebox.showwarning(title="Redo Error", message="Nothing to redo")

    def copy(self, event=None) -> None:
        self.window.clipboard_clear()
        content = self.text.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        self.window.clipboard_append(content)

    def cut(self, event=None) -> None:
        self.copy()
        self.text.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)

    def paste(self, event=None) -> None:
        content = self.window.clipboard_get()
        self.text.insert(tkinter.INSERT, content)

    def select_all(self, event=None) -> None:
        self.text.tag_add(tkinter.SEL, 1.0, tkinter.END)

    def initialize(self) -> None:
        self.window.title("Notepad--")
        self.window.iconphoto(True, self.icons.app_icon)
        self.window.config(menu=self.menu_bar,
                           bg="#000000")
        self.window.protocol("WM_DELETE_WINDOW", self.exit)
        self.menu_bar.add_cascade(label="File",
                                  menu=self.file_menu)
        self.file_menu.add_command(label="New",
                                   command=self.new_file,
                                   image=self.icons.new_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + N")
        self.file_menu.add_command(label="Open",
                                   command=self.open_file,
                                   image=self.icons.open_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + O")
        self.file_menu.add_command(label="Save",
                                   command=self.save_file,
                                   image=self.icons.save_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + S")
        self.file_menu.add_command(label="Save As...",
                                   command=self.save_file_as,
                                   image=self.icons.save_file_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + Shift + S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",
                                   command=self.exit,
                                   image=self.icons.exit_icon,
                                   compound=tkinter.LEFT)
        self.menu_bar.add_cascade(label="Edit",
                            menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo",
                                   accelerator="Ctrl + Z",
                                   command=self.undo,
                                   image=self.icons.undo_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Redo",
                                   accelerator="Ctrl + Y",
                                   command=self.redo,
                                   image=self.icons.redo_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Clear",
                                   command=self.clear_file,
                                   image=self.icons.clear_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + Shift + Delete")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut",
                                   accelerator="Ctrl + X",
                                   command=self.cut,
                                   image=self.icons.cut_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Copy",
                                   accelerator="Ctrl + C",
                                   command=self.copy,
                                   image=self.icons.copy_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_command(label="Paste",
                                   accelerator="Ctrl + V",
                                   command=self.paste,
                                   image=self.icons.paste_icon,
                                   compound=tkinter.LEFT)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find",
                                   command=self.find,
                                   image=self.icons.find_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + F")
        self.edit_menu.add_command(label="Find & Replace",
                                   command=self.find_and_replace,
                                   image=self.icons.find_and_replace_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + H")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Generate Random Text",
                                   command=self.generate_random_text,
                                   image=self.icons.generate_random_text_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Ctrl + G")
        self.edit_menu.add_command(label="Toggle Word Wrap",
                                   command=self.toggle_word_wrap,
                                   image=self.icons.word_wrap_icon,
                                   compound=tkinter.LEFT,
                                   accelerator="Alt + Z")
        self.font_style_menu.add_command(label="Normal",
                                          command=lambda: self.change_font_style("normal"))
        self.font_style_menu.add_command(label="Bold",
                                          command=lambda: self.change_font_style("bold"))
        self.font_style_menu.add_separator()
        self.font_style_menu.add_command(label="Roman",
                                          command=lambda: self.change_font_style("roman"))
        self.font_style_menu.add_command(label="Italic",
                                         command=lambda: self.change_font_style("italic"))
        self.menu_bar.add_cascade(label="Appearance",
                                  menu=self.appearance_menu)
        self.appearance_menu.add_command(label="Reset",
                                         command=self.set_preferences_to_default,
                                         image=self.icons.reset_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Themes",
                                         command=self.manage_themes,
                                         image=self.icons.themes_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Background Color",
                                         command=self.change_background_color,
                                         image=self.icons.change_background_color_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Font Color",
                                         command=self.change_font_color,
                                         image=self.icons.change_font_color_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Font Family",
                                         image=self.icons.change_font_family_icon,
                                         compound=tkinter.LEFT,
                                         command=self.change_font_family)
        self.appearance_menu.add_cascade(label="Change Font Style",
                                         menu=self.font_style_menu,
                                         image=self.icons.change_font_style_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_command(label="Change Font Size",
                                         command=self.change_font_size,
                                         image=self.icons.change_font_size_icon,
                                         compound=tkinter.LEFT)
        self.appearance_menu.add_separator()
        self.appearance_menu.add_command(label="Save Preferences",
                                         command=self.save_preferences,
                                         image=self.icons.save_file_icon,
                                         compound=tkinter.LEFT)
        self.text.pack(expand=True, fill=tkinter.BOTH)
        self.characters_count_label.grid(row=0, column=0, pady=5, padx=5)
        self.words_count_label.grid(row=0, column=1, padx=75, pady=5)
        self.counters_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.window.bind("<KeyRelease>", self.count_characters_and_words)
        self.main_frame.pack(expand=True, fill=tkinter.BOTH)
        self.load_themes()
        self.load_preferences()
        self.window.update()
        self.window.attributes("-zoomed", True)
        self.window.bind("<Control-h>", self.find_and_replace)
        self.window.bind("<Control-f>", self.find)
        self.window.bind("<Control-s>", self.save_file)
        self.window.bind("<Control-Shift-S>", self.save_file_as)
        self.window.bind("<Control-n>", self.new_file)
        self.window.bind("<Control-o>", self.open_file)
        self.window.bind("<Alt-z>", self.toggle_word_wrap)
        self.window.bind("<Control-Shift-Delete>", self.clear_text)
        self.window.bind("<Control-g>", self.generate_random_text)
        self.window.bind("<Control-a>", self.select_all)
        self.window.mainloop()

if __name__ == "__main__":
    notepad = Notepad()
    notepad.initialize()