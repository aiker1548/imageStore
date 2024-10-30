import os
import shutil

def save_file(file, destination):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return destination
