import mailbox
import time
#https://pymotw.com/2/mailbox/
from email.utils import parsedate_tz, mktime_tz

def parseMbox(locationName, beginTimeFrame = 0, endTimeFrame = int(time.time())):

    mbox = mailbox.mbox(locationName)
    listOfMails = []
    for message in mbox:
        try:
            timestamp = mktime_tz(parsedate_tz(message['date']))
            if int(timestamp) < endTimeFrame and int(timestamp) > beginTimeFrame:
                #http://stackoverflow.com/questions/12160010/email-datetime-parsing-with-python
                mailInfo = timestamp, 'Mbox', \
                    "From: " + str(message['from']) + ", " \
                    "To: " + str(message['to']) + ", " \
                    "Subject: " + str(message['subject'])
                listOfMails.append(mailInfo)
        except TypeError:
            pass

    return listOfMails