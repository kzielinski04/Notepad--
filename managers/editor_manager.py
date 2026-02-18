import tkinter
import tkinter.messagebox
import random
import time

class EditorManager:
    def __init__(self, notepad):
        self.characters_count = 0
        self.words_count = 0
        self.line_number = 0
        self.column_number = 0
        self.notepad = notepad
        self.file_manager = None

    def add_file_manager(self, file_manager):
        self.file_manager = file_manager

    def clear_file(self, event=None) -> None:
        """Clears file with confirmation"""
        if self.text_is_empty():
            tkinter.messagebox.showwarning(title="Empty File", message="This file is empty")
            return
        if tkinter.messagebox.askyesno(title="Clearing Document", message="Are you sure you want to clear this file?"):
            self.notepad.text.delete(1.0, tkinter.END)
        else:
            return
    
    def clear_text(self, event=None) -> None:
        """Clears file without confirmation"""
        self.notepad.text.delete(1.0, tkinter.END)

    def text_is_empty(self) -> bool:
        return len(self.notepad.text.get(1.0, tkinter.END)) - 1 == 0
    
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
                self.notepad.text.tag_remove(tkinter.SEL, tkinter.SEL_FIRST, tkinter.SEL_LAST)
            except Exception:
                pass
            if matches:
                for m in enumerate(matches):
                    self.notepad.text.tag_remove("match_found", m[1][0], m[1][1])
            matches.clear()

            def next_match(event=None):
                if matches:
                    current_selection_start_index.set(self.notepad.text.index(tkinter.SEL_FIRST))
                    current_selection_end_index.set(self.notepad.text.index(tkinter.SEL_LAST))
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
                    self.notepad.text.tag_remove(tkinter.SEL, current_selection_start_index.get(), current_selection_end_index.get())
                    self.notepad.text.tag_add(tkinter.SEL, new_selection_start_index, new_selection_end_index)
                    current_selection_start_index.set(new_selection_start_index)
                    current_selection_end_index.set(new_selection_end_index)

            def previous_match(event=None):
                if matches:
                    current_selection_start_index.set(self.notepad.text.index(tkinter.SEL_FIRST))
                    current_selection_end_index.set(self.notepad.text.index(tkinter.SEL_LAST))
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
                    self.notepad.text.tag_remove(tkinter.SEL, current_selection_start_index.get(), current_selection_end_index.get())
                    self.notepad.text.tag_add(tkinter.SEL, new_selection_start_index, new_selection_end_index)
                    current_selection_start_index.set(new_selection_start_index)
                    current_selection_end_index.set(new_selection_end_index)

            find_previous_button = tkinter.Button(find_frame,
                                          font=self.notepad.main_font,
                                          text="<-",
                                          command=previous_match)
            find_previous_button.grid(row=1, column=0)
            find_button.grid(row=1, column=1)
            find_next_button = tkinter.Button(find_frame,
                                          font=self.notepad.main_font,
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
                text_match_index = self.notepad.text.search(find_text, start_index, tkinter.END)
                if not text_match_index:
                    break
                match_count += 1
                self.notepad.text.tag_add("match_found",
                                text_match_index,
                                f"{text_match_index}+{len(find_text)}c")
                self.notepad.text.tag_config("match_found", background="yellow")
                current_match = (text_match_index, f"{text_match_index}+{len(find_text)}c")
                matches.append(current_match)
                start_index = f"{text_match_index}+{len(find_text)}c"
            if match_count != 0:
                self.notepad.text.tag_add(tkinter.SEL, matches[0][0], matches[0][1])
                current_selection_start_index.set(self.notepad.text.index(tkinter.SEL_FIRST))
                current_selection_end_index.set(self.notepad.text.index(tkinter.SEL_LAST))
                match_count_label = tkinter.Label(find_window,
                                                font=self.notepad.main_font,
                                                text=f"1/{match_count}")
            else:
                match_count_label = tkinter.Label(find_window,
                                                font=self.notepad.main_font,
                                                text="0/0")
            match_count_label.grid(row=2, column=0, columnspan=3)
            
        def find_exit():
            if matches:
                for m in matches:
                    self.notepad.text.tag_remove("match_found", m[0], m[1])
            find_window.destroy()

        find_window = tkinter.Toplevel(self.notepad.window)
        find_window.title("Find")
        find_window.resizable(False, False)
        find_window.protocol("WM_DELETE_WINDOW", find_exit)
        find_label = tkinter.Label(find_window,
                                   font=self.notepad.main_font,
                                   text="Enter the text to find: ")
        find_entry = tkinter.Entry(find_window,
                                   font=self.notepad.main_font)
        find_label.grid(row=0, column=0, pady=5)
        find_entry.grid(row=0, column=1, pady=5)
        find_frame = tkinter.Frame(find_window)
        find_button = tkinter.Button(find_frame,
                                     font=self.notepad.main_font,
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
            content = self.notepad.text.get(1.0, tkinter.END)
            find = find_entry.get()
            replace = replace_entry.get()
            result = content.replace(find, replace)
            match_count = content.count(find)
            if match_count == 0:
                tkinter.messagebox.showinfo(title="No Matches", message="No matches found")
                return
            find_and_replace_progress_bar.grid(row=3, column=0, columnspan=2)
            find_and_replace_progress_bar_label.grid(row=4, column=0, columnspan=2)
            find_and_replace_window.update()
            replaced_count = 0
            while replaced_count < match_count:
                find_and_replace_progress_bar["value"] += (100 / match_count)
                percent.set(f"{int((replaced_count * 100) / match_count)}%")
                time.sleep(0.01)
                replaced_count += 1
                find_and_replace_window.update_idletasks()
            self.clear_text()
            self.notepad.text.insert(1.0, result)
            tkinter.messagebox.showinfo(title="Find & Replace Completed", message=f"Replaced {match_count} occurences")
            find_and_replace_window.destroy()
        if self.text_is_empty():
            tkinter.messagebox.showwarning(title="Empty File", message="This file is empty")
            return
        find_and_replace_window = tkinter.Toplevel(self.notepad.window)
        find_and_replace_window.title("Find & Replace")
        find_and_replace_window.resizable(False, False)
        find_label = tkinter.Label(find_and_replace_window,
                                   text="Enter the text to find: ",
                                   font=self.notepad.main_font)
        find_label.grid(row=0,
                        column=0,
                        pady=5)
        find_entry = tkinter.Entry(find_and_replace_window,
                                   font=self.notepad.main_font)
        find_entry.grid(row=0,
                        column=1,
                        pady=5)
        replace_label = tkinter.Label(find_and_replace_window,
                                   text="Enter the text to replace: ",
                                   font=self.notepad.main_font)
        replace_label.grid(row=1,
                           column=0,
                           pady=5)
        replace_entry = tkinter.Entry(find_and_replace_window,
                                   font=self.notepad.main_font)
        replace_entry.grid(row=1,
                           column=1,
                           pady=5)
        submit_button = tkinter.Button(find_and_replace_window,
                                       text="Find & Replace",
                                       command=execute,
                                       font=self.notepad.main_font)
        submit_button.grid(row=2,
                           column=0,
                           columnspan=2,
                           pady=5)
        percent = tkinter.StringVar(value="0%")
        find_and_replace_progress_bar = tkinter.ttk.Progressbar(find_and_replace_window,
                                                                orient=tkinter.HORIZONTAL,
                                                                length=300)
        find_and_replace_progress_bar_label = tkinter.Label(find_and_replace_window,
                                                            textvariable=percent)
        find_and_replace_window.bind("<Return>", execute)

    def generate_random_text(self, event=None) -> None:
        def generate_random_text_execute(event=None):
            content = self.notepad.text.get(1.0, tkinter.END) 
            if (len(content) - 1) != 0 and content != self.file_manager.saved_content:
                choice = tkinter.messagebox.askyesno(message="Do you want to save your file before generating the random text?")
                if choice:
                    if len(self.file_manager.saved_file_path) == 0:
                        self.file_manager.save_file_as()
                    else:
                        self.file_manager.save_file()
            length = random_text_length_entry.get()
            if not length.isdigit() or int(length) == 0:
                tkinter.messagebox.showwarning(title="Input Error", message="Length must be a positive number")
                return
            length = int(length)
            result = ""
            for i in range(length):
                result = result + chr(random.randint(32, 126))
            self.clear_text()
            self.notepad.text.insert(1.0, result)
            generate_random_text_window.destroy()

        generate_random_text_window = tkinter.Toplevel(self.notepad.window)
        generate_random_text_window.title("Generate Random Text")
        random_text_length_label = tkinter.Label(generate_random_text_window,
                                                 font=self.notepad.main_font,
                                                 text="Enter the length of the random text: ")
        random_text_length_label.grid(row=0,
                                      column=0,
                                      pady=5)
        random_text_length_entry = tkinter.Entry(generate_random_text_window,
                                                 font=self.notepad.main_font)
        random_text_length_entry.grid(row=0,
                                      column=1,
                                      pady=5)
        generate_random_text_button = tkinter.Button(generate_random_text_window,
                                                     font=self.notepad.main_font,
                                                     text="Generate",
                                                     command=generate_random_text_execute)
        generate_random_text_button.grid(row=1,
                                         column=0,
                                         columnspan=2,
                                         pady=5)
        generate_random_text_window.bind("<Return>", generate_random_text_execute)

    def update_footer_stats(self, event=None) -> None:
        position = self.notepad.text.index(tkinter.INSERT)
        self.line_number, self.column_number = position.split(".")
        self.notepad.line_number_label.config(text=f"Line: {self.line_number}")
        self.notepad.column_number_label.config(text=f"Column: {self.column_number}")
        content = self.notepad.text.get(1.0, "end-1c")
        char_counter = 0
        for c in content:
            if c != " ":
                char_counter = char_counter + 1
        self.characters_count = char_counter
        self.notepad.characters_count_label.config(text=f"Characters: {self.characters_count}")

        content = content.split()
        words_counter = len(content)
        self.words_count = words_counter
        self.notepad.words_count_label.config(text=f"Words: {self.words_count}")

    def undo(self, event=None) -> None:
        try:
            self.notepad.text.edit_undo()
        except tkinter.TclError:
            tkinter.messagebox.showwarning(title="Undo Error", message="Nothing to undo")

    def redo(self, event=None) -> None:
        try:
            self.notepad.text.edit_redo()
        except tkinter.TclError:
            tkinter.messagebox.showwarning(title="Redo Error", message="Nothing to redo")

    def copy(self, event=None) -> None:
        try:
            self.notepad.window.clipboard_clear()
            content = self.notepad.text.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            self.notepad.window.clipboard_append(content)
        except tkinter.TclError:
            tkinter.messagebox.showwarning(title="No Selection Error", message="No text was selected to copy")

    def cut(self, event=None) -> None:
        try:
            self.notepad.window.clipboard_clear()
            content = self.notepad.text.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            self.notepad.window.clipboard_append(content)
            self.notepad.text.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
        except tkinter.TclError:
            tkinter.messagebox.showwarning(title="No Selection Error", message="No text was selected to cut")

    def paste(self, event=None) -> None:
        try:
            content = self.notepad.window.clipboard_get()
            self.notepad.text.insert(tkinter.INSERT, content)
        except tkinter.TclError:
            tkinter.messagebox.showwarning(title="Empty Clipboard Error", message="No text to paste")

    def select_all(self, event=None) -> None:
        self.notepad.text.tag_add(tkinter.SEL, 1.0, tkinter.END)