import os
from tkinter import Frame
from ui_components import ShellText
from command_executor import execute_command

class ShellInterface(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.current_dir = os.getcwd()
        self.text = ShellText(self, execute_callback=self.execute_with_state)
        self.text.pack(fill="both", expand=True)

    def execute_with_state(self, command):
        output, new_dir = execute_command(command, self.current_dir)
        if new_dir:
            self.current_dir = new_dir
        return output
