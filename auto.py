from keep_alive import keep_alive
import http.client
import json
import random
import sys
import time
from time import sleep
from http.client import HTTPSConnection
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def configure_info():
    try:
        user_id = os.getenv("USERID") or input("User-ID: ")
        token = os.getenv("TOKEN") or input("Discord token: ")
        channel_url = os.getenv("URL") or input("Discord channel URL: ")
        channel_id = os.getenv("ID") or input("Discord channel ID: ")

        # Set environment variables
        os.environ["USERID"] = user_id
        os.environ["TOKEN"] = token
        os.environ["URL"] = channel_url
        os.environ["ID"] = channel_id
    except Exception as e:
        print(f"Error configuring user information: {e}")
        exit()

def set_channel():
    user_id = os.getenv("USERID")
    token = os.getenv("TOKEN")
    channel_url = input("Discord channel URL: ")
    channel_id = input("Discord channel ID: ")
    os.environ["URL"] = channel_url
    os.environ["ID"] = channel_id

def show_help():
    print("Showing help for discord-auto-messenger")
    print("Usage:")
    print("  'python3 auto.py'               :  Runs the automessenger. Type in the wait time and take a back seat.")
    print("  'python3 auto.py --config'      :  Configure settings.")
    print("  'python3 auto.py --setC'  :  Set channel to send message to. Including Channel ID and Channel URL")
    print("  'python3 auto.py --help'        :  Show help")

if len(sys.argv) > 1:
    if sys.argv[1] == "--config" and input("Configure? (y/n)") == "y":
        configure_info()
        exit()
    elif sys.argv[1] == "--setC" and input("Set channel? (y/n)") == "y":
        set_channel()
        exit()
    elif sys.argv[1] == "--help":
        show_help()
        exit()

header_data = {
    "content-type": "application/json",
    "user-id": os.getenv("USERID"),
    "authorization": os.getenv("TOKEN"),
    "host": "discordapp.com",
    "referrer": os.getenv("URL")
}

print("Messages will be sent to " + header_data["referrer"] + ".")

def get_connection():
    return HTTPSConnection("discordapp.com", 443)

def send_message(conn, channel_id, message_data):
    try:
        conn.request("POST", f"/api/v6/channels/{channel_id}/messages", message_data, header_data)
        resp = conn.getresponse()

        if 199 < resp.status < 300:
            print("Message sent!")
    except Exception as e:
        print(f"Error sending message: {e}")

# Read messages from file
with open("messages.txt", "r") as file:
    messages = file.read()

message_data = json.dumps({"content": messages})

# Read server IDs from user
server_ids = input("Enter the server IDs (comma-separated) to send the message to: ").split(',')

# Establish connection
conn = get_connection()

while True:
    for server_id in server_ids:
        send_message(conn, server_id.strip(), message_data)
        print(f"Message sent to server ID: {server_id.strip()}")

    wait_time = int(input("Seconds until next message (or 0 to stop): "))
    if wait_time == 0:
        break

    print(f"Waiting {wait_time} seconds...")
    time.sleep(wait_time)

conn.close()
