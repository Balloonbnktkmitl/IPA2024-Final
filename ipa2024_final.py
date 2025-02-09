#######################################################################################
# Yourname:
# Your student ID:
# Your GitHub Repo: 

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import requests
import json
import time
import os

from requests_toolbelt.multipart.encoder import MultipartEncoder
from netmiko_final import gigabit_status
from restconf_final import create, delete, enable, disable, status
from ansible_final import showrun
#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
if ACCESS_TOKEN is None:
    raise ValueError("Webex Access Token: Not found, please set it in the environment variables.")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vZjRlYzBlZDAtZTJkMC0xMWVlLWFhZDAtNDNlNTUwYjg4Mzhj"

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": "Bearer " + ACCESS_TOKEN}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages", 
        params=getParameters, 
        headers=getHTTPHeader, 
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.find("/65070021") == 0:

        # extract the command
        command = message.split(" ", 1) # Add
        command = command[1] # Add
        print(command)

# 5. Complete the logic for each command

        if command == "create":
            responseMessage = create()
        elif command == "delete":
            responseMessage = delete()
        elif command == "enable":
            responseMessage = enable()
        elif command == "disable":
            responseMessage = disable()
        elif command == "status":
            responseMessage = status()
        elif command == "gigabit_status":
            responseMessage = gigabit_status()
        elif command == "showrun":
            responseMessage = showrun()
        else:
            responseMessage = "Error: No command or unknown command"
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            filename = "show_run_65070021_CSR1KV-Pod1-1.txt"
            fileobject = open(filename, 'rb')
            filetype = 'text/plain'
            postData = {
                "roomId": roomIdToGetMessages,
                "text": "show running config",
                "files": (filename, fileobject, filetype),
            }
            postData = MultipartEncoder(fields=postData)
            postHTTPHeaders= HTTPHeaders = {
            "Authorization": "Bearer " + ACCESS_TOKEN,
            "Content-Type": postData.content_type,
            }
        
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": roomIdToGetMessages, "text": responseMessage} 
            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            postHTTPHeaders = HTTPHeaders = {"Authorization": "Bearer " + ACCESS_TOKEN, "Content-Type": "application/json"}
            postData=json.dumps(postData)
            

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages", 
            data=postData, 
            headers=postHTTPHeaders, 
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
