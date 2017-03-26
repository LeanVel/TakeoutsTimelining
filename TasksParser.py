import json
import time

def parseTasks(tasksFile, begintimeframe = 0, endtimeframe = int(time.time())) :

    tasksList = json.load(open(tasksFile, 'r'))

    listOfTasks = []

    for tasks in tasksList["items"]:

        taskListTitle= tasks["title"]
        timeStamp = tasks["updated"]

        timeStamp = (int(time.mktime(time.strptime(timeStamp, '%Y-%m-%dT%H:%M:%S.000Z'))) - time.timezone)

        # time filtering
        if timeStamp < endtimeframe and timeStamp > begintimeframe:

            for task in tasks["items"]:

                timeStamp = task["updated"]
                timeStamp = (int(time.mktime(time.strptime(timeStamp, '%Y-%m-%dT%H:%M:%S.000Z'))) - time.timezone)
                title = task["title"]
                try :
                    notes = task["notes"]
                except :
                    notes = ""
                try:
                    dueDate = task["due"]
                except:
                    dueDate = ""

                taskInfo = timeStamp, 'Tasks', \
                    "Tasks List Title: " + taskListTitle + ", " \
                    "Task Title: " + title + ", " \
                    "Task notes: " + notes + ", " \
                    "Due date: " + dueDate

                listOfTasks.append(taskInfo)

    return listOfTasks
