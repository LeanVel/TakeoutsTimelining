from lxml import html
import time


def parseStream (filename, beginTimeFrame = 0, endTimeFrame = int(time.time())) :
    listOfStream = []

    file = open(filename, 'r')
    html_info = html.fromstring(file.read())
    title = html_info.xpath('//div[@class="original-content"]/text()')
    published = html_info.xpath('//abbr[@class="published"]/@title')
    unixTimeStamp = int(time.mktime(time.strptime(published[0], '%Y-%m-%dT%H:%M:%S.%fZ')))

    if int(unixTimeStamp) < endTimeFrame and int(unixTimeStamp) > beginTimeFrame:
        #print(title[0])
        #print(published[0])
        #print(unixTimeStamp)
        streamInfo = int(unixTimeStamp), 'Stream', \
            "Title: " + str(title[0])
        listOfStream.append(streamInfo)
    file.close()
    return listOfStream