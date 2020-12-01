import os
import time 
import config
import importlib

running = True

def startprog():

    if config.src_path is None:
        print("path not found")
        config.error = "path not found"
        exit(1)

    try:
        import watchdog.events    
        import watchdog.observers
    except:
        config.error = "ERROR: Dependancy not installed. Please run PIP Install watchdog"
        exit(1)    
    try:
        from PIL import Image 
    except:
        config.error = "ERROR: Dependancy not installed. Please run PIP Install pillow"
        exit(1)     

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

    event_handler = Handler() 
    observer = watchdog.observers.Observer() 
    observer.schedule(event_handler, path=config.src_path, recursive=True) 
    observer.start() 

    while running is True: 
        time.sleep(1) 
    if running is False: 
        observer.stop() 
        if len(imagelist) == 0:
            config.message = "No images received!"
            print("No images received!")
            exit(0)
        img1 = imagelist[0]    
        if len(imagelist) == 1:
            img1.save(r"spydf_{time}.pdf".format(time = time.strftime("%H_%M_%S", time.localtime())))
            config.message = "PDF succesfully created!"
            print("PDF succesfully created!")
            exit(0)  
        elif len(imagelist) > 1:  
            imagelist.pop(0)
            img1.save(r"spydf_{time}.pdf".format(time = time.strftime("%H_%M_%S", time.localtime())), save_all = True, append_images=imagelist)
            print("PDF succesfully created!")
            config.message = "PDF succesfully created!"
            exit(0) 
    config.running = True
    exit(0)     
