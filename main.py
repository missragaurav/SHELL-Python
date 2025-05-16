import tkinter as tk
from shell_interface import ShellInterface

def main():
    root = tk.Tk()
    root.title("Custom Python Shell")
    root.geometry("700x400")

    shell = ShellInterface(root)
    shell.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
