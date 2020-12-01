import os
import time 

try:
    import watchdog.events    
    import watchdog.observers
except:
    print("ERROR: Dependancy not installed. Please run PIP Install watchdog")
    exit(1)    
try:
    from PIL import Image 
except:
    print("ERROR: Dependancy not installed. Please run PIP Install pillow")
    exit(1)     


print("Welcome to SPYDF \n All your Screenshots to PDF through Python \n Script sucessfully started, press ^C to terminate\n")

imagelist = list()

class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self): 
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png'], ignore_directories=True, case_sensitive=False) 
            
  
    def on_created(self, event): 
        print("Received Screenshot - % s." % event.src_path) 
        
        filepath = str(event.src_path)
        try:
            image = Image.open(filepath, mode="r").convert("RGB")
            imagelist.append(image)
        except:
            pass  

if __name__ == "__main__": 

    try:
        with open("spydf_path.txt", "r") as file:
            src_path = file.readlines()[0]
    except:
        with open("spydf_path.txt", "w") as file:
            src_path = input("Enter the path of ScreenShots Folder> ")
            file.write(src_path)
            print("Path Set! Screenshot Capturing Started. Press ^C to exit")

    event_handler = Handler() 
    observer = watchdog.observers.Observer() 
    observer.schedule(event_handler, path=src_path, recursive=True) 
    observer.start() 
    try: 
        while True: 
            time.sleep(1) 
    except KeyboardInterrupt: 
        observer.stop() 
        if len(imagelist) == 0:
            print("No images received!")
            input("Press any key to exit> ") 

        img1 = imagelist[0]    

        if len(imagelist) == 1:
            img1.save(r"file.pdf")
            print("Done!, find out your pdf named file.pdf")    

        elif len(imagelist) > 1:  
            imagelist.pop(0)
            img1.save(r"spydf_{time}.pdf".format(time = time.strftime("%H_%M_%S", time.localtime())), save_all = True, append_images=imagelist)
            print("Done!, find out your pdf named file.pdf")

        input("Press any key to exit> ")    
    observer.join() 
