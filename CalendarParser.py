from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC
from DBManager import initDB,insertSingleRecord,printTable,insertMultipleRecords
import time

def parseCalendar (calName, begintimeframe = 0, endtimeframe = int(time.time())) :

    listOfEvents = []

    calFile = open(calName, 'r')
    cal = Calendar.from_ical(calFile.read())

    for component in cal.walk():

        if component.name == "VEVENT":

            dateCreated = str((component.decoded('created')))

            #convert from datetime to epoch
            dateCreated = (int(time.mktime(time.strptime(dateCreated, '%Y-%m-%d %H:%M:%S+00:00'))) - time.timezone)

            if dateCreated < endtimeframe and dateCreated > begintimeframe:

                summary = (component.get('summary'))
                description = (component.get('description'))
                location = (component.get('location'))

                dateLastModified = str((component.decoded('last-modified')))
                dateStart = str((component.decoded('dtstart')))
                dateEnd = str((component.decoded('dtend')))
                dateStamp = str((component.decoded('dtstamp')))

                #organizer can be emptyG
                try:
                    organizer = str((component.decoded('organizer')))
                except :
                    organizer = ""

                #attendee can be empty
                attendees=""
                try:
                    attendeeList = (component.get('attendee'))
                    for attendee in attendeeList:
                        attendees += str(attendee) +  ", "
                except :
                    attendees = ""

                #prepare string containing event info to append it to the list

                #for multiple inserts
                eventInfo = dateCreated, 'Calendar', \
                    "Summary: " + summary + ", "\
                    "Description: " + description + ", "\
                    "Start date: " + dateStart + ", " \
                    "End date: " + dateEnd + ", " \
                    "STAMP date: " + dateStamp + ", " \
                    "Last Modification date: " + dateLastModified + ", " \
                    "Location: " + location + ", " \
                    "Organizer: " + organizer + ", " \
                    "Attendees: " + attendees

                listOfEvents.append(eventInfo)

                # for inidividual inserts:

                # eventInfo = (datecreated, 'Calendar',
                #     "Summary: " + summary + ", "\
                #     "Description: " + description + ", "\
                #     "Start date: " + dateStart + ", " \
                #     "End date: " + dateEnd + ", " \
                #     "STAMP date: " + dateStamp + ", " \
                #     "Last Modification date: " + dateLastModified + ", " \
                #     "Location: " + location + ", " \
                #     "Organizer: " + organizer + ", " \
                #     "Attendees: " + attendees ),

                # insertSingleRecord(eventInfo)

                #print in stdout

                # print ("Summary:" + summary + "\n" \
                #        "Description:" + description + "\n" \
                #        "Start date: " + dateStart + "\n" \
                #        "End date: " + dateEnd + "\n" \
                #        "STAMP date: " + dateStamp + "\n" \
                #        "Creation date: " + dateCreated + "\n" \
                #        "Last Modification date: " + dateLastModified + "\n" \
                #        "Location: " + location + "\n" \
                #        "Organizer: " + organizer + "\n" \
                #        "Attendees: " + attendees + "\n" \
                #        )

    calFile.close()
    return listOfEvents