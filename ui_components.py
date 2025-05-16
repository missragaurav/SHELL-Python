import tkinter as tk

class ShellText(tk.Text):
    def __init__(self, master, execute_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.execute_callback = execute_callback
        self.insert("end", "$ ")
        self.mark_set("input_start", "insert")
        self.bind("<Return>", self.handle_enter)
        self.bind("<BackSpace>", self.handle_backspace)
        self.bind("<Key>", self.handle_key)
        self.cmd_start = self.index("insert")
        self.focus_set()

    def handle_enter(self, event):
        command = self.get("input_start", "end-1c").strip()
        output = self.execute_callback(command)
        self.insert("end", "\n" + output + "$ ")
        self.mark_set("input_start", "end-2c")
        self.see("end")
        return "break"

    def handle_backspace(self, event):
        if self.compare("insert", "<=", "input_start"):
            return "break"

    def handle_key(self, event):
        if self.compare("insert", "<", "input_start"):
            self.mark_set("insert", "end")
