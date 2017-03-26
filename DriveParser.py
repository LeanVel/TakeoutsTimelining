import os
import time

def list_files(path):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files

def parseDrive(filename, beginTimeFrame = 0, endTimeFrame = int(time.time())):

    listOfDrive = []

    # for file in list_files(locationName):
        #st_mtime only works on linux systems http://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
    timestamp = int(os.stat(filename).st_mtime)

    if int(timestamp) < endTimeFrame and int(timestamp) > beginTimeFrame:
        fileInfo = timestamp, 'Drive', \
            "Filename: " + str(filename) + ", " \
            "Modified: " + str(timestamp)
        listOfDrive.append(fileInfo)

    return listOfDrive