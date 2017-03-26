import json
import datetime
import os
import time
from DBManager import insertMultipleRecords, initDB

def parseLocation (locationName, beginTimeFrame = 0, endTimeFrame = int(time.time())) :

    begintimeframe = beginTimeFrame*1000
    endtimeframe = endTimeFrame*1000


    data = json.load(open(locationName,'r'))
    #print(data)

    #print("Timestamp" + "\t" + "latitude" + "\t" + "longitude" + "\t" + "accuracy"  + "\t" + "altitude")

    # for location in data["locations"]:
        #print(str(location["timestampMs"]) + "\t" + str(location["latitudeE7"]) + "\t" + str(location["longitudeE7"]) + "\t" + str(location["accuracy"]) + "\t\t" + str(location["altitude"]))

    #Start of Leandro addition for insertions in the DB

    listOfLocation = []

    for location in data["locations"]:
        if int(location["timestampMs"]) < endtimeframe and int(location["timestampMs"]) > begintimeframe:
            unixTimeStamp = int(location["timestampMs"])/1000
            locationInfo = int(unixTimeStamp), 'Location History', \
                "Latitude: " + str(location["latitudeE7"]/10000000) + ", "\
                "Longitude: " + str(location["longitudeE7"]/10000000) + ", "\
                "Altitude: " + str(location["altitude"]) + ", " \
                "Accuracy: " + str(location["accuracy"])

            listOfLocation.append(locationInfo)

    #When this script is transformed into a function (that will be called from the main programm)
    # the following instroctions wont be necesarry and te fuction should return the list.

    return listOfLocation



# def generateLocationHtml(locationName,filename = "locationHistoryMap"):
#
#
#     # data = json.load(open(locationName, 'r'))
#
#     with open("output/"+ filename+".html", 'w') as outfile:
#         with open('includes/location/header') as header:
#             for line in header:
#                 outfile.write(line)
#         head = ""
#         for location in locationName["locations"]:
#             head += "<a href='javascript:map.setCenter (new OpenLayers.LonLat( " + str(location["longitudeE7"]/10000000) + ", " + str(location["latitudeE7"]/10000000) + " ).transform(epsg4326, projectTo), 16);'>" + str(datetime.datetime.utcfromtimestamp(int(location["timestampMs"])/1000.0)) + "Z UTC</a><br />"
#         outfile.write(head)
#
#         for data in locationName:
#
#             split_data = data[2].split(",")
#             tmp_data = split_data[1] + split_data[0]
#             tmp_data = tmp_data.replace("Latitude:", "")
#             tmp_data = tmp_data.replace("Longitude:", "")
#             tmp_data = tmp_data[2:].replace(" ", ", ")
#             # print(tmp_data)
#
#             head += "<tr><td>" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data[0])) + "</td><td>" + str(data[1]) + "</td><td>" + str(data[2]) + " <a href=\"#\" onclick=\"openOverlay( " + tmp_data + " )\">Show</a></td></tr> \n"
#
#
#         with open('includes/location/middle') as middle:
#             for line in middle:
#                 outfile.write(line)
#
#         #add markers here
#         for location in data["locations"]:
#
#             latitude = str(location["latitudeE7"]/10000000)
#             longtitude = str(location["longitudeE7"]/10000000)
#             marker = """    var feature = new OpenLayers.Feature.Vector(
#                 new OpenLayers.Geometry.Point( """
#             marker += longtitude
#             marker += """, """
#             marker += latitude
#             marker += """ ).transform(epsg4326, projectTo),
#                 {description:'"""
#
#             try:
#                 marker += "timestamp: " + str(datetime.datetime.utcfromtimestamp(int(location["timestampMs"])/1000.0)) + " accuracy: " + str(location["accuracy"]) + " altitude: " + str(location["altitude"])
#             except KeyError:
#                 marker += "timestamp: " + str(
#                     datetime.datetime.utcfromtimestamp(int(location["timestampMs"]) / 1000.0)) + " accuracy: " + str(location["accuracy"])
#             marker += """'} ,
#                 {externalGraphic: '../includes/img/marker.png', graphicHeight: 25, graphicWidth: 21, graphicXOffset:-12, graphicYOffset:-25  }
#             );
#         vectorLayer.addFeatures(feature);
#         """
#             outfile.write(marker)
#
#         with open('includes/location/footer') as footer:
#             for line in footer:
#                 outfile.write(line)
#
#     os.system("firefox output/map.html")
