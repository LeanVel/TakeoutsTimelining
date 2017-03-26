#!/usr/bin/python3.5
# System imports
import zipfile
import subprocess
import optparse
import os
import os.path
import datetime, time
from CalendarParser import parseCalendar
from LocationParser import parseLocation
from MboxParser import parseMbox
# from DBManager import initDB,insertSingleRecord,printTable,insertMultipleRecords
from OutputManager import initOutput, insertMultipleRecords,generateOutput,generateHTMLLocation
from SearchesParser import parseSearches
from DriveParser import parseDrive
from HangoutsParser import parseHangouts
from TasksParser import parseTasks
from StreamParser import parseStream
import shutil
import glob
import sys

# Link for the wiki
# https://www.os3.nl/2016-2017/students/leandro_velasco/ccf/project?&#alice_log

#TODO Integrate DBManager with the OutputManager

def main(takeoutFiles, destDir, dbName, beginTimeFrame, endTimeFrame, outDir, outPrefix):

    uncompressTakeout(takeoutFiles, destDir)

    # initDB(dbName)

    initOutput(outDir,outPrefix)

    parseTakout(destDir,beginTimeFrame, endTimeFrame)

    generateOutput()

def parseTakout(destDir,beginTimeFrame, endTimeFrame) :
    takeoutFilePath = destDir + "/Takeout"

    try :
        dirs = os.listdir(takeoutFilePath)
    except FileNotFoundError :
        sys.exit("File does not exist")

    for dir in dirs:

        if (dir == "Calendar"):
            files = os.listdir(takeoutFilePath+"/"+dir)
            for file in files:
                filePath = takeoutFilePath+"/"+dir+"/"+file
                print("Parsing "+filePath)
                data = parseCalendar(filePath, beginTimeFrame, endTimeFrame)
                insertMultipleRecords(data)
        elif (dir == "Hangouts") :
            files = os.listdir(takeoutFilePath + "/" + dir)
            for file in files:
                filePath = takeoutFilePath + "/" + dir + "/" + file
                print("Parsing " + filePath)
                data = parseHangouts(filePath, beginTimeFrame, endTimeFrame)
                insertMultipleRecords(data)
        elif (dir == "Location History"):
            files = os.listdir(takeoutFilePath + "/" + dir)
            for file in files:
                filePath = takeoutFilePath + "/" + dir + "/" + file
                print("Parsing " + filePath)
                data = parseLocation(filePath, beginTimeFrame,endTimeFrame)
                insertMultipleRecords(data)
                generateHTMLLocation(data)
        elif (dir == "Mail") :
            files = os.listdir(takeoutFilePath + "/" + dir)
            for file in files:
                filePath = takeoutFilePath + "/" + dir + "/" + file
                print("Parsing " + filePath)
                data = parseMbox(filePath, beginTimeFrame, endTimeFrame)
                insertMultipleRecords(data)
        elif (dir == "Searches") :
            files = os.listdir(takeoutFilePath + "/" + dir)
            for file in files:
                filePath = takeoutFilePath + "/" + dir + "/" + file
                print("Parsing " + filePath)
                data = parseSearches(filePath, beginTimeFrame, endTimeFrame)
                insertMultipleRecords(data)
        elif (dir == "Tasks") :
            files = os.listdir(takeoutFilePath + "/" + dir)
            for file in files:
                filePath = takeoutFilePath + "/" + dir + "/" + file
                print("Parsing " + filePath)
                data = parseTasks(filePath, beginTimeFrame, endTimeFrame)
                insertMultipleRecords(data)
        elif (dir == "Drive") :
            files = os.listdir(takeoutFilePath + "/" + dir)
            for file in files:
                filePath = takeoutFilePath + "/" + dir + "/" + file
                print("Parsing " + filePath)
                data = parseDrive(filePath, beginTimeFrame, endTimeFrame)
                insertMultipleRecords(data)
        elif (dir == "Google+ Stream"):
            files = os.listdir(takeoutFilePath + "/" + dir)
            for file in files:
                filePath = takeoutFilePath + "/" + dir + "/" + file
                print("Parsing " + filePath)
                data = parseStream(filePath, beginTimeFrame, endTimeFrame)
                insertMultipleRecords(data)
        else:
            print (dir + " Not supported")

    #old Version!
 # for subDir, dirs, files in os.walk(destDir+"/Takeout"):
    #     for file in files:
    #         subDirList = subDir.split('/')
    #
    #         prefixLength = len(destDir.split('/'))
    #
    #         if len(subDirList) > 2 :
    #             gService =subDirList[prefixLength+1]
                # if (gService == "Calendar"):
                #     print("Parsing "+os.path.join(subDir, file))
                #     data = parseCalendar(os.path.join(subDir, file), beginTimeFrame, endTimeFrame)
                #     insertMultipleRecords(data)
                # elif (gService == "Hangouts") :
                #     print("Parsing " + os.path.join(subDir, file))
                #     data = parseHangouts(os.path.join(subDir, file), beginTimeFrame, endTimeFrame)
                #     insertMultipleRecords(data)
                # elif (gService == "Location History"):
                #     print("Parsing " + os.path.join(subDir, file))
                #     data = parseLocation(os.path.join(subDir, file), beginTimeFrame,endTimeFrame, allOutputs)
                #     insertMultipleRecords(data)
                #     generateHTMLLocation(data)
                # elif (gService == "Mail") :
                #     print("Parsing " + os.path.join(subDir, file))
                #     data = parseMbox(os.path.join(subDir, file), beginTimeFrame, endTimeFrame)
                #     insertMultipleRecords(data)
                # elif (gService == "Searches") :
                #     print("Parsing " + os.path.join(subDir, file))
                #     data = parseSearches(os.path.join(subDir, file), beginTimeFrame, endTimeFrame)
                #     insertMultipleRecords(data)
                # elif (gService == "Tasks") :
                #     print("Parsing " + os.path.join(subDir, file))
                #     data = parseTasks(os.path.join(subDir, file), beginTimeFrame, endTimeFrame)
                #     insertMultipleRecords(data)
                # elif  (gService == "Drive") :
                #     print("Parsing " + os.path.join(subDir, file))
                #     data = parseDrive(os.path.join(subDir, file), beginTimeFrame, endTimeFrame)
                #     insertMultipleRecords(data)
                # elif (gService == "Google+ Stream"):
                #     print("Parsing " + os.path.join(subDir, file))
                #     data = parseStream(os.path.join(subDir, file), beginTimeFrame, endTimeFrame)
                #     insertMultipleRecords(data)
                # else:
                #     print (gService + " Not supported")

def uncompressTakeout(takeoutFiles, destDir) :

    try:
        shutil.rmtree(destDir + "/Takeout")
    except FileNotFoundError:
        # print(destDir + "/Takeout Directory was not already created")
        pass

    for files in takeoutFiles :

        for file in (glob.glob(os.path.expanduser(files),recursive=True)):

            print ("Sha256 of the "+file+" file:")
            subprocess.call(['sha256sum', file])

            fileName, fileExtention = os.path.splitext(file)

            if fileExtention==".zip":
                subprocess.call(['unzip', '-o' ,'-d', destDir, file])
            elif (fileExtention== ".tgz") | (fileExtention==".tbz") :
                subprocess.call(['tar', '-xf', file, '--directory='+destDir])
            else :
                print (fileExtention + " File format not supported")

    #this code modified the "Creation time"
    # zfile = zipfile.ZipFile(file)
    # for name in zfile.namelist():
    #     (dirname, filename) = os.path.split(name)
    #     print("Decompressing " + filename + " on " + destDir+"/"+dirname)
    #     if not os.path.exists(destDir+"/"+dirname):
    #         os.makedirs(destDir+"/"+dirname)
    #     zfile.extract(name, destDir)

if __name__ == "__main__":

    parser = optparse.OptionParser("usage: %prog [options] <TakeOut File(s)>")

    parser.add_option("-d", "--dest-dir", dest="destDir",
                    default = "/tmp", type = "string",
                    help = "specify destination directory to decompress the takeout file")

    parser.add_option("-o", "--output-dest-dir", dest="outDir",
                    default = "./", type = "string",
                    help = "specify destination directory to save the output files")

    parser.add_option("-p", "--output-prefix", dest="outPrefix",
                    default = "output", type = "string",
                    help = "specify the output files prefix")

    # parser.add_option("-D", "--DB-name", dest="dbName",
    #                 default = "mydatabase.db", type = "string",
    #                 help = "specify database name (if it exists it will use the specified one )")

    parser.add_option("-b", "--beging-time-frame", dest="beginTimeFrame",
                    type = "string",
                    help = "specify the begining of the desired time frame in the format YYYY-MM-DD hh:mm")

    parser.add_option("-e", "--end-time-frame", dest="endTimeFrame",
                    default = datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), type = "string",
                    help = "specify the end of the desired time frame in the format YYYY-MM-DD hh:mm")

    (options, args) = parser.parse_args()

    if len(args) < 1 :
        parser.error("incorrect number of arguments")

    # If no beginTimeFrame Specified default to 0
    if options.beginTimeFrame != None :

        try :
            beginTimeFrame = int(time.mktime(datetime.datetime.strptime(options.beginTimeFrame, "%Y-%m-%d %H:%M").timetuple()))
        except ValueError:
            beginTimeFrame = 0
            print ("Wrong time format, assuming: "+ str(beginTimeFrame)+ "for begining date-time of the time frame")
    else:
        beginTimeFrame = 0

    try :
        endTimeFrame = int(time.mktime(datetime.datetime.strptime(options.endTimeFrame, "%Y-%m-%d %H:%M").timetuple()))
    except ValueError:
        endTimeFrame = int(time.time())
        print("Wrong time format, assuming current date-time: " + str(endTimeFrame) + "for the end date-time of the time frame")

    # dbName = options.dbName
    dbName = ""

    main(args,options.destDir, dbName, beginTimeFrame, endTimeFrame,options.outDir,options.outPrefix)