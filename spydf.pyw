from tkinter import *
from tkinter.filedialog import askdirectory 
import spydf_gui
import threading
import config
import importlib

def main():
    def update(text):
        status.set(text)

    def set_path(): 
        path = askdirectory()
        with open ("spydf_path.txt", "w") as file:
            file.write(path)
        importlib.reload(config)        
        update(f"Path Set: {path}")

    def start():        
        t2 = threading.Thread(target=spydf_gui.startprog) 
        t2.start()
        if config.error is not None:
            update(config.error)
        else:    
            update("Program Running")

    
    def stop():
        spydf_gui.running = False
        importlib.reload(config)
        exit(0)
        


    #gui
    root = Tk()

    status = StringVar()
    if config.src_path is None:
        status.set("Please set the path before starting")
    else:
        status.set("Program Sucessfully Loaded")

    root.title("SPYDF")
    root.geometry("350x200")
    root.minsize(350, 200)
    root.maxsize(350, 200)

    #Title
    f1 = Frame(root)
    l1 = Label(f1, text = "SPYDF", font = "arialblack 20 bold")
    f1.pack()
    l1.pack(fill = "x", pady = 10)

    #bottombar
    f2 = Frame(root, bg = "green", height = 20)
    f2.pack(side = "bottom", fill = "x")
    l2 = Label(f2, textvariable = status, font = "arial 10 bold")
    l2.pack()

    #button1
    f3 = Frame(root)
    b1 = Button(f3, text = "Set Path", font = "bold",bd = 1, width = 10, height = 1, command = lambda:set_path())
    f3.pack(side = "left", anchor = "n", padx = 10)
    b1.pack(pady = 10)

    #button2
    f4 = Frame(root)
    b2 = Button(f4, text = "Start", font = "bold",bd = 1, width = 10, height = 1, command = lambda:start())
    f4.pack(side = "left", anchor = "n", fill = "x", padx = 10)
    b2.pack(pady = 10, fill = "x")

    #button3
    f5 = Frame(root)
    b3 = Button(f5, text = "Stop", font = "bold",bd = 1, width = 10, height = 1, command = lambda:stop())
    f5.pack(side = "left", anchor = "n", padx = 10)
    b3.pack(pady = 10)

    root.mainloop()
    #gui end

if __name__ == "__main__":
    t1 = threading.Thread(target=main) 
    t1.start()    
