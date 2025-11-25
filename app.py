from tkinter import *
from tkinter import filedialog
import subprocess


class Window(Frame):
    def __init__(self, master=None, anch=LEFT):
        Frame.__init__(self, master, width=200, height=200)
        self.master = master

        self.pack(fill=BOTH, expand=True)

        self.text = Text(self, height=200, width=200)
        self.text.pack(side=LEFT, fill=BOTH, expand=True)

        #self.scrollbar = Scrollbar(top, orient="vertical")
        #self.scrollbar.config(command=self.text.yview)
        #self.scrollbar.pack(side=RIGHT, fill=Y, expand=True)
#
        #self.text.config(yscrollcommand=self.scrollbar.set)

    def open_file_function(self):

        #self.file_save = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("txt files", "*.txt"), ("All files", "*.*")))
        with open('systems.txt') as file:
            for i in file:
                self.text.insert(END, i)
            file.close()

    def save_file_function(self) -> None:
        with open('systems.txt', 'w') as file:
            text_content = self.text.get("1.0", 'end-1c')
            file.write(text_content)
            file.close()

    def run_router(self) -> None:
        subprocess.run(command)
        self.text.config(state=NORMAL)
        if(len(self.text.get("1.0", 'end-1c')) > 0):
            self.text.delete(1.0, END)
        with open('route.txt') as file:
            for i in file:
                self.text.insert(END, i)
            file.close()
        self.text.config(state=DISABLED)
        
class Buttons(Frame):
    def __init__(self, master=None, anch=LEFT):
        Frame.__init__(self, master, width=200, height=200)
        self.master = master

        self.pack(fill=X, expand=True)
        isLoop, isSpansh, isJson, isGreedy  = IntVar(), IntVar(), IntVar(), IntVar()
        button_loop = Checkbutton(self, text='Loop',variable=isLoop, onvalue=1, offvalue=0, command=lambda: self.set_command(isLoop, button_loop))
        button_spansh = Checkbutton(self, text='Spansh',variable=isSpansh, onvalue=1, offvalue=0, command=lambda: self.set_command(isSpansh, button_spansh))
        button_json = Checkbutton(self, text='JSON output',variable=isJson, onvalue=1, offvalue=0, command=lambda: self.set_command(isJson, button_json))
        button_greedy = Checkbutton(self, text='Use greedy algorithm',variable=isGreedy, onvalue=1, offvalue=0, command=lambda: self.set_command(isGreedy, button_greedy))
        button_loop.pack()
        button_spansh.pack()
        button_json.pack()
        button_greedy.pack()



    def set_command(self, var:IntVar=None, button:Checkbutton=None) -> None:
        match button.config('text')[-1]:
            case "Loop":
                if(var.get() == 1):
                    command.append("-l")
                else:
                    command.remove("-l")
            case "Spansh":
                if(var.get() == 1):
                    command.append("-s")
                else:
                    command.remove("-s")
            case "JSON output":
                if(var.get() == 1):
                    command.append("-j")
                else:
                    command.remove("-j")
            case "Use greedy algorithm":
                if(var.get() == 1):
                    command.append("-g")
                else:
                    command.remove("-g")
            case _:
                print("Skill issue")

def make_menus(l_frame, r_frame):
        file_menu = Menu(top)
        top.config(menu=file_menu)
        l_frame.file_menu = Menu(file_menu)
        file_menu.add_cascade(label="File", menu=l_frame.file_menu)
        l_frame.file_menu.add_command(label="New")
        l_frame.file_menu.add_command(label="Open",      command=l_frame.open_file_function)
        l_frame.file_menu.add_command(label="Save", command=l_frame.save_file_function)
        l_frame.file_menu.add_separator()
        l_frame.file_menu.add_command(label="Exit")

        r_frame.router = Menu(file_menu)
        file_menu.add_cascade(label="Router", menu=r_frame.router)
        r_frame.router.add_command(label="Run",      command=r_frame.run_router)
        r_frame.router.add_separator()
        r_frame.router.add_command(label="Exit")

top = Tk()
top.geometry("1000x500")
top.title("Elite: Dangerous Router")
command = ["router.exe"]
main_frame = Frame(top)
main_frame.pack(fill=BOTH, expand=1, side=TOP)
l_frame = Window(main_frame)
l_frame.pack(side=LEFT)
l_frame.pack_propagate(0)
r_frame = Window(main_frame)
r_frame.pack(side=RIGHT)
r_frame.pack_propagate(0)
make_menus(l_frame, r_frame)
low_frame = Buttons(top)
low_frame.pack(side=BOTTOM)
low_frame.pack_propagate(0)

top.mainloop()
