import requests

"""
1. Create a credentials.yml file and put rest: as the first line in the file.
2. Create endpoints.yml file and put the following

action_endpoint:
  url: 'http://localhost:5055/webhook'

3. Start up Rasa with: rasa run -m models --endpoints endpoints.yml --port 5002
  --credentials credentials.yml
  
4. Run below python script.
"""
sender = input("What is your name?\n")

bot_message = ""
while bot_message != "Bye":
    message = input("What's your message?\n")
    print("Sending message now...")
    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"sender": sender, "message": message})
    print("Bot says, ")
    recognized_intent = r.json()[0]['text']
    print(recognized_intent)

