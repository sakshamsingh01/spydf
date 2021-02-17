import os
import time 
import config
import importlib
import watchdog.events   
import watchdog.observers
from PIL import Image
import ctypes.wintypes

#to get user's documents path
CSIDL_PERSONAL = 5      
SHGFP_TYPE_CURRENT = 0   

buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

path = buf.value.replace("/", "\\") +"\\"+"spydf"

if not os.path.exists(path):
    os.mkdir(path)

running = True

def startprog():

    if config.src_path is None:
        config.error = "path not found"
        exit(1)

    imagelist = list()

    class Handler(watchdog.events.PatternMatchingEventHandler): 
        def __init__(self): 
            watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.png'], ignore_directories=True, case_sensitive=False) 
    
        def on_created(self, event):  
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
            exit(0)
        img1 = imagelist[0]    
        if len(imagelist) == 1:
            img1.save(r"{destination}\spydf_{time}.pdf".format(time = time.strftime("%H_%M_%S", time.localtime())), destination=path.replace("/", "\\"))
            exit(0)  
        elif len(imagelist) > 1:  
            imagelist.pop(0)
            img1.save(r"{}\spydf_{}.pdf".format(path, time.strftime("%H_%M_%S", time.localtime())), save_all = True, append_images=imagelist)
            exit(0) 
    exit(0)     
