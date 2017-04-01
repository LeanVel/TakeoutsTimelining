import csv
import time
import datetime
import os
from shutil import copyfile
import json

def initOutput(outputDirs, outFilename):
    # global variable list
    global list
    global filename
    global outputDir

    outputDir = outputDirs+"/output"

    list = []
    filename = outFilename

    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    copyfile("includes/img/marker.png", outputDir+"/marker.png")

def insertMultipleRecords(data):
    list.extend(data)


def generateOutput():
    list.sort()
    generateCSV()
    generateHTML()
    generateJson()
    print("Output generated at :"+outputDir)

def generateJson():
    with open(outputDir+"/"+filename+".json", 'w') as myfile:
        json.dump(list, myfile)

def generateCSV():
    with open(outputDir+"/"+filename+".csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for tuple in list :
            wr.writerow(tuple)


def generateHTML():

    output = """
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <style>
    body {
        margin: 0;
        font-family: 'Lato', sans-serif;
    }

    .overlay {
        height: 100%;
        width: 100%;
        position: fixed;
        z-index: 1;
        top: 0;
        left: 0;
        background-color: rgb(0,0,0);
        background-color: rgba(0,0,0, 0.9);
        display: none;
        overflow-x: hidden;
        transition: 0.5s;
    }

    .overlay-content {
        position: relative;
        top: 25%;
        width: 100%;
        text-align: center;
        margin-top: 30px;
    }

    .overlay a {
        padding: 8px;
        text-decoration: none;
        font-size: 36px;
        color: #810000;
        display: block;
        transition: 0.3s;
        z-index: 10000;
    }

    .overlay a:hover, .overlay a:focus {
        color: #BB0000;
    }

    .overlay .closebtn {
        position: absolute;
        top: 50px;
        right: 45px;
        font-size: 60px;
    }

    @media screen and (max-height: 450px) {
      .overlay a {font-size: 20px}
      .overlay .closebtn {
        font-size: 40px;
        top: 15px;
        right: 35px;
      }
    }
    table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 60%;
        position: relative;
        margin-left: auto;
        margin-right: auto;
    }

    tbody td {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }
    thead th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even) {
        background-color: #dddddd;
    }
    </style>
    </head>
    <body>
    <script src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
    <script src="http://www.openlayers.org/api/OpenLayers.js"></script>
    <div id="MapOverlay" class="overlay">
      <a href="javascript:void(0)" class="closebtn" onclick="closeOverlay()">&times;</a>

    </div>

    <table id="timeline" class="display">
    <thead>
      <tr>
        <th>Timestamp (UTC +00)</th>
        <th>Event type</th>
        <th>Details</th>
      </tr>
    </thead>
    <tbody>
    """

    for data in list:
        if data[1] == "Location History":
            split_data = data[2].split(",")
            tmp_data = split_data[1] + split_data[0]
            tmp_data = tmp_data.replace("Latitude:", "")
            tmp_data = tmp_data.replace("Longitude:", "")
            tmp_data = tmp_data[2:].replace(" ", ", ")
            #print(tmp_data)

            output += "<tr><td>" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(data[0])) + "</td><td>" + str(data[1]) + "</td><td>" + str(data[2]) + " <a href=\"#\" onclick=\"openOverlay( " + tmp_data + " )\">Show</a></td></tr> \n"
        else:
            output += "<tr><td>" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(data[0])) + "</td><td>" + str(data[1]) + "</td><td>" + str(data[2]) + "</td></tr> \n"

    output += """
    </tbody>
    </table>

    <script>
    $(document).ready(function(){
        $('#timeline').DataTable();
    });

    function openOverlay(Lon, Lat) {
        document.getElementById("MapOverlay").style.display = "block";
        document.getElementById("timeline").style.display = "none";
        map = new OpenLayers.Map("MapOverlay");
        map.addLayer(new OpenLayers.Layer.OSM());

        epsg4326 =  new OpenLayers.Projection("EPSG:4326"); //WGS 1984 projection
        projectTo = map.getProjectionObject(); //The map projection (Spherical Mercator)

        var lonLat = new OpenLayers.LonLat( Lon, Lat ).transform(epsg4326, projectTo);


        var zoom=15;
        map.setCenter (lonLat, zoom);

        var vectorLayer = new OpenLayers.Layer.Vector("Overlay");

        // Define markers as "features" of the vector layer:
        var feature = new OpenLayers.Feature.Vector(
                new OpenLayers.Geometry.Point( Lon, Lat ).transform(epsg4326, projectTo),
                {description:'description'} ,
                {externalGraphic: 'marker.png', graphicHeight: 25, graphicWidth: 21, graphicXOffset:-12, graphicYOffset:-25  }
            );

        vectorLayer.addFeatures(feature);

        map.addLayer(vectorLayer);


        //Add a selector control to the vectorLayer with popup functions
        var controls = {
          selector: new OpenLayers.Control.SelectFeature(vectorLayer, { onSelect: createPopup, onUnselect: destroyPopup })
        };

        function createPopup(feature) {
          feature.popup = new OpenLayers.Popup.FramedCloud("pop",
              feature.geometry.getBounds().getCenterLonLat(),
              null,
              '<div class="markerContent">'+feature.attributes.description+'</div>',
              null,
              true,
              function() { controls['selector'].unselectAll(); }
          );
          //feature.popup.closeOnMove = true;
          map.addPopup(feature.popup);
        }

        function destroyPopup(feature) {
          feature.popup.destroy();
          feature.popup = null;
        }

        map.addControl(controls['selector']);
        controls['selector'].activate();
        map.setCenter (new OpenLayers.LonLat( Long, Lat ).transform(epsg4326, projectTo), 16);
    }

    function closeOverlay() {
        document.getElementById("MapOverlay").style.display = "none";
        document.getElementById("timeline").style.display = "block";
    }
    </script>

    </body>
    </html>
    """

    with open(outputDir+"/"+filename+".html", 'w') as outfile:
        # for line in output:
        outfile.write(output)


def generateHTMLLocation(locationData):

    outputHead = """<html>
  <head><title>OpenLayers Marker Popups</title>
  <style>body, html { height:100%; padding:0; margin:0;}</style>
  </head>
  <body>
  <div style="float:left; width:20%; height:100%; background: #eeeeee; overflow-y: scroll;">
    """
    outputLeftMenu = ""
    outputJavaScript = ""

    for data in locationData:
        if data[1] == "Location History":

            split_data = data[2].split(",")
            tmp_data = split_data[1] + split_data[0]
            tmp_data = tmp_data.replace("Latitude:", "")
            tmp_data = tmp_data.replace("Longitude:", "")
            tmp_data = tmp_data[2:].replace(" ", ", ")
            #print(tmp_data)
            timestamp = str(datetime.datetime.utcfromtimestamp(int(data[0])))
            outputLeftMenu += "<a href='javascript:map.setCenter (new OpenLayers.LonLat( " + tmp_data + " ).transform(epsg4326, projectTo), 16);'>" + timestamp + "Z UTC</a><br />"

            outputJavaScript += """ var feature = new OpenLayers.Feature.Vector(
                    new OpenLayers.Geometry.Point( """+ tmp_data + """ ).transform(epsg4326, projectTo),
                    {description:'""" + timestamp + """ """ + data[2] + """'} ,
                    {externalGraphic: 'marker.png', graphicHeight: 25, graphicWidth: 21, graphicXOffset:-12, graphicYOffset:-25  }
                );
            vectorLayer.addFeatures(feature);
            """

    outputMiddle = """</div>
  <div id="mapdiv" style="overflow:hidden; width:80%; height:100%;"></div>
  <script src="http://www.openlayers.org/api/OpenLayers.js"></script>
  <script>
    map = new OpenLayers.Map("mapdiv");
    map.addLayer(new OpenLayers.Layer.OSM());

    epsg4326 =  new OpenLayers.Projection("EPSG:4326"); //WGS 1984 projection
    projectTo = map.getProjectionObject(); //The map projection (Spherical Mercator)

    var lonLat = new OpenLayers.LonLat( 8.683333, 50.116667 ).transform(epsg4326, projectTo);


    var zoom=5;
    map.setCenter (lonLat, zoom);

    var vectorLayer = new OpenLayers.Layer.Vector("Overlay");

    // Define markers as "features" of the vector layer:

    """

    outputTail = """    map.addLayer(vectorLayer);


    //Add a selector control to the vectorLayer with popup functions
    var controls = {
      selector: new OpenLayers.Control.SelectFeature(vectorLayer, { onSelect: createPopup, onUnselect: destroyPopup })
    };

    function createPopup(feature) {
      feature.popup = new OpenLayers.Popup.FramedCloud("pop",
          feature.geometry.getBounds().getCenterLonLat(),
          null,
          '<div class="markerContent">'+feature.attributes.description+'</div>',
          null,
          true,
          function() { controls['selector'].unselectAll(); }
      );
      //feature.popup.closeOnMove = true;
      map.addPopup(feature.popup);
    }

    function destroyPopup(feature) {
      feature.popup.destroy();
      feature.popup = null;
    }

    map.addControl(controls['selector']);
    controls['selector'].activate();

  </script>

</body></html>"""

    with open(outputDir+"/"+filename+"Location.html", 'w') as outfile:
        # for line in output:
        outfile.write(outputHead+outputLeftMenu+outputMiddle+outputJavaScript+outputTail)
