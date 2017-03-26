import time
import json

def parseHangouts(locationName, beginTimeFrame = 0, endTimeFrame = int(time.time())):

    data = json.load(open(locationName,'r'))
    conversations = []
    for conversation in data['conversation_state']:
        participantsarray = []
        participantsdict={}
        #participants
        for participants in conversation['conversation_state']['conversation']['participant_data']:

            participantsdict[participants['id']['gaia_id']] = participants['fallback_name']
            participantsarray.append(participants['fallback_name'])

        for message in conversation['conversation_state']['event']:
            try:
                #original timestap is in microseconds that is why we need to devide the value by 1000000
                timestamp = int(message['timestamp'])//1000000
                if int(timestamp) < endTimeFrame and int(timestamp) > beginTimeFrame:

                    hangoutsInfo = timestamp, 'Hangouts', \
                        "From: " + str(participantsdict[message['sender_id']['gaia_id']]) + ", " \
                        "Message: " + str(message['chat_message']['message_content']['segment'][0]['text']) + ", " \
                        "Participants: " + str(participantsarray)
                    conversations.append(hangoutsInfo)

            except KeyError:
                pass

    return conversations
