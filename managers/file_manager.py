import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import os.path

class FileManager:
    def __init__(self, notepad):
        self.saved_content = ""
        self.saved_file_path = ""
        self.notepad = notepad
        self.editor_manager = None
        self.is_auto_save_enabled = False
        self.auto_save_delay = None

    def add_editor_manager(self, editor_manager):
        self.editor_manager = editor_manager

    def text_is_empty(self) -> bool:
        return len(self.notepad.text.get(1.0, tkinter.END)) - 1 == 0

    def clear_text(self, event=None) -> None:
        """Clears file without confirmation"""
        self.notepad.text.delete(1.0, tkinter.END)

    def clear_file(self, event=None) -> None:
        """Clears file with confirmation"""
        if self.editor_manager.text_is_empty():
            tkinter.messagebox.showwarning(title="Empty File", message="This file is empty")
            return
        if tkinter.messagebox.askyesno(title="Clearing Document", message="Are you sure you want to clear this file?"):
            self.notepad.text.delete(1.0, tkinter.END)
        else:
            return

    def new_file(self, event=None) -> None:
        file_content = self.notepad.text.get(1.0, "end-1c")
        if (len(file_content) - 1) != 0 and file_content != self.saved_content:
            choice = tkinter.messagebox.askyesno(message="Do you want to save your file before creating a new one?")
            if choice:
                self.save_file_as()
        self.clear_text()
        self.notepad.file_name_label.config(text="File: Unnamed File")

    def open_file(self, event=None) -> None:
        file_content = self.notepad.text.get(1.0, "end-1c")
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
                self.clear_text()
                self.notepad.text.insert(1.0, content)
                self.notepad.file_name_label.config(text=f"File: {os.path.basename(file_path)}")

                

    def toggle_auto_save(self, event=None) -> None:
        def toggle_auto_save_execute(event=None):
            if not auto_save_delay_entry.get():
                tkinter.messagebox.showwarning(title="Empty Input", message="Auto Save delay value not entered")
                return
            self.auto_save_delay = int(auto_save_delay_entry.get())
            tkinter.messagebox.showinfo(title="Auto Save ON",
                                        message="Auto Save is now enabled")
            self.is_auto_save_enabled = True
            auto_save_window.destroy()

        if self.is_auto_save_enabled:
            tkinter.messagebox.showinfo(title="Auto Save OFF",
                                        message="Auto Save is now disabled")
            self.is_auto_save_enabled = False
            self.auto_save_delay = None
        else:
            auto_save_window = tkinter.Toplevel(self.notepad.window)
            auto_save_window.resizable(False, False)
            auto_save_delay_label = tkinter.Label(auto_save_window,
                                                  font=self.notepad.main_font,
                                                  text="Enter Auto Save delay (ms): ")
            auto_save_delay_entry = tkinter.Entry(auto_save_window,
                                                  font=self.notepad.main_font)
            submit_button = tkinter.Button(auto_save_window,
                                           font=self.notepad.main_font,
                                           text="Submit",
                                           command=toggle_auto_save_execute)
            auto_save_delay_label.grid(row=0, column=0, pady=5)
            auto_save_delay_entry.grid(row=0, column=1, pady=5)
            submit_button.grid(row=1, column=0, columnspan=2, pady=5)
            auto_save_window.bind("<Destroy>", self.auto_save)
            auto_save_window.bind("<Return>", toggle_auto_save_execute)

    def auto_save(self, event=None) -> None:
        if self.is_auto_save_enabled:
            self.save_file()
            self.notepad.window.after(self.auto_save_delay, self.auto_save)

    def save_file(self, event=None) -> None:
        if not self.saved_file_path:
            self.save_file_as()
        else:
            with open(self.saved_file_path, "w") as f:
                content = self.notepad.text.get(1.0, "end-1c")
                f.write(content)
                self.saved_content = content
                self.notepad.file_name_label.config(text=f"File: {os.path.basename(self.saved_file_path)}")

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
            content = self.notepad.text.get(1.0, "end-1c")
            f.write(content)
            self.saved_content = content
            self.notepad.file_name_label.config(text=f"File: {os.path.basename(self.saved_file_path)}")

    def exit(self) -> None:
        file_content = self.notepad.text.get(1.0, "end-1c")
        if (len(file_content) - 1) != 0 and file_content != self.saved_content:
            choice = tkinter.messagebox.askyesno(message="Do you want to save your file before exit?")
            if choice:
                if not self.saved_file_path:
                    self.save_file_as()
                else:
                    self.save_file()
        current_font = tkinter.font.Font(font=self.notepad.text["font"])
        current_preferences = {
            "background_color": self.notepad.text["bg"],
            "font_color": self.notepad.text["fg"],
            "font_family": current_font["family"],
            "font_weight": current_font["weight"],
            "font_slant": current_font["slant"],
            "font_size": current_font["size"],
            "word_wrap_on": self.notepad.preferences_manager.word_wrap_on,
            "auto_save_on": self.notepad.file_manager.is_auto_save_enabled,
            "auto_save_delay": self.notepad.file_manager.auto_save_delay
        }
        for (cp, sp) in zip(current_preferences.values(), self.notepad.preferences_manager.saved_preferences.values()):
            if cp != sp:
                choice = tkinter.messagebox.askyesno(message="Do you want to save your preferences before exit?")
                if choice:
                    self.notepad.preferences_manager.save_preferences()
                break        
        self.notepad.window.quit()