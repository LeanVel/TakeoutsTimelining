import json
import time

def parseSearches(searchesFile, begintimeframe = 0, endtimeframe = int(time.time())) :

    searches = json.load(open(searchesFile, 'r'))

    listOfsearches = []

    for search in searches["event"]:
        #a query can contain several timestap so special measurments need te be implemented in order to handle it

        for timeStampDic in search["query"]['id'] :

            timeStamp = int(timeStampDic["timestamp_usec"]) // 1000000

            # time filtering
            if timeStamp < endtimeframe and timeStamp > begintimeframe:

                #timeStamp =  timeStamp / 1000
                queryText = str(search["query"]["query_text"])

                searchInfo = timeStamp, 'Searches', \
                    "Query Text: " + queryText

                listOfsearches.append(searchInfo)

    return listOfsearches