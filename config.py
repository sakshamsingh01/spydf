error = None
try:
    with open("spydf_path.txt", "r") as file:
        src_path = file.readlines()[0].replace("/", "\\")
except:
    error =  "Error: Path not set"
    src_path = None
