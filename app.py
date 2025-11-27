import os
import threading
import subprocess
from tkinter import *
from tkinter import filedialog
from dotenv import load_dotenv, set_key


class Window(Frame):
    time = 0
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

    def refresh(self, i):
        self.master.update()
        i += 1
        if('Done' in loading_label['text']):
            self.time = 0
            pass
        elif('/ Loading' in loading_label['text']):
            loading_label['text'] = f'\\ Loading {i}s'
            self.time = i
            self.master.after(1000,self.refresh, i)
        else:
            loading_label['text'] = f'/ Loading {i}s'
            self.time = i
            self.master.after(1000,self.refresh, i)

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

    def split_tasks(self):
        loading_label['text'] = ''
        self.refresh(0)
        threading.Thread(target=self.run_router).start()

    def run_router(self) -> None:
        subprocess.run(command)
        self.text.config(state=NORMAL)
        if(len(self.text.get("1.0", 'end-1c')) > 0):
            self.text.delete(1.0, END)
        with open(os.path.join(OUTPUT_PATH, 'route.txt')) as file:
            for i in file:
                self.text.insert(END, i)
            file.close()
        self.text.config(state=DISABLED)
        loading_label['text'] = f"Done in {self.time}s ! "

        
class Buttons(Frame):
    def __init__(self, master=None, anch=LEFT):
        Frame.__init__(self, master, width=200, height=200)
        self.master = master
        global save_location, loading_label
        self.pack(fill=X, expand=True)
        isLoop, isSpansh, isJson, isGreedy  = IntVar(), IntVar(), IntVar(), IntVar()
        button_loop = Checkbutton(self, text='Loop',variable=isLoop, onvalue=1, offvalue=0, command=lambda: self.set_command(isLoop, button_loop))
        button_spansh = Checkbutton(self, text='Spansh',variable=isSpansh, onvalue=1, offvalue=0, command=lambda: self.set_command(isSpansh, button_spansh))
        button_json = Checkbutton(self, text='JSON output',variable=isJson, onvalue=1, offvalue=0, command=lambda: self.set_command(isJson, button_json))
        button_greedy = Checkbutton(self, text='Use greedy algorithm',variable=isGreedy, onvalue=1, offvalue=0, command=lambda: self.set_command(isGreedy, button_greedy))
        button_save = Button(self, text='Save output', command=self.select_save_path)
        save_location = Label(self, text=OUTPUT_PATH)
        loading_label = Label(self, text='')
        loading_label.pack(side=BOTTOM, pady=10)
        save_location.pack(side=RIGHT, padx=20)
        button_save.pack(side=RIGHT, padx=20)
        button_loop.pack(side=LEFT)
        button_spansh.pack(side=LEFT)
        button_json.pack(side=LEFT)
        button_greedy.pack(side=LEFT)


    def select_save_path(self):
        self.file_save = filedialog.askdirectory(initialdir = "/", title = "Select file")
        global OUTPUT_PATH
        OUTPUT_PATH = str(self.file_save)
        save_location['text'] = self.file_save
        set_key('.env', 'OUTPUT_PATH', self.file_save)
        load_dotenv()

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
        file_menu.add_cascade(label="File", menu=l_frame.file_menu, )
        l_frame.file_menu.add_command(label="Open",      command=l_frame.open_file_function)
        l_frame.file_menu.add_command(label="Save", command=l_frame.save_file_function)
        l_frame.file_menu.add_separator()
        #l_frame.file_menu.add_command(label="Exit")

        r_frame.router = Menu(file_menu)
        #file_menu.add_cascade(label="Router", menu=r_frame.router)
        file_menu.add_command(label='Run router', command=lambda:[l_frame.save_file_function(), r_frame.split_tasks()])
        #r_frame.router.add_command(label="Run",      command=r_frame.run_router)
        #r_frame.router.add_separator()
        #r_frame.router.add_command(label="Exit")


def redefine_save(path:str):
    if(path == '%USERPROFILE%\\Downloads\\'):
        path = path.replace(str('%USERPROFILE%'), str(os.getenv('USERPROFILE')))
        set_key('.env', 'OUTPUT_PATH', path)
        os.environ['OUTPUT_PATH'] = path
        load_dotenv()
        return path
    else:
        return path

global OUTPUT_PATH
load_dotenv()
OUTPUT_PATH = os.getenv('OUTPUT_PATH', '')
OUTPUT_PATH = redefine_save(OUTPUT_PATH)
top = Tk()
top.geometry("1000x500")
top.title("Elite: Dangerous Router")
command = ["router.exe"]
main_frame = Frame(top)
main_frame.pack(fill=BOTH, expand=1, side=TOP)
l_frame = Window(main_frame)
l_frame.pack(side=LEFT)
l_frame.open_file_function()
l_frame.pack_propagate(0)
r_frame = Window(main_frame)
r_frame.pack(side=RIGHT)
r_frame.pack_propagate(0)
make_menus(l_frame, r_frame)
low_frame = Buttons(top)
low_frame.pack(side=BOTTOM)
low_frame.pack_propagate(0)

top.mainloop()
