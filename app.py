from tkinter import *
from tkinter import filedialog

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.master.title("Notepad")
        self.pack(fill=BOTH, expand=1)

        menu = Menu(top)
        top.config(menu=menu)
        self.file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Open",      command=self.open_file_function)
        self.file_menu.add_command(label="Save", command=self.save_file_function)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")

        self.text = Text(top, height=200, width=200)
        self.text.pack(side=LEFT, fill=Y, expand=True)
        self.text2 = Text(top, height=200, width=200)
        self.text2.pack(side=RIGHT, fill=Y, expand=True)

        self.scrollbar = Scrollbar(top, orient="vertical")
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=True)

        self.text.config(yscrollcommand=self.scrollbar.set)


    def open_file_function(self):

        #self.file_save = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("txt files", "*.txt"), ("All files", "*.*")))
        with open('systems.txt') as file:
            for i in file:
                self.text.insert(END, i)

    def save_file_function(self) -> None:
        pass


top = Tk()
top.geometry("500x500")
ap = Window(top)
ap2 = Window(top)

top.mainloop()
