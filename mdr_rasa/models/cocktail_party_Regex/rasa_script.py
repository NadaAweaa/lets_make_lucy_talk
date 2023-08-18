import subprocess
import time
import requests
from rasa.nlu.model import Interpreter


rasa_run = "rasa run"
rasa_train = "rasa train"

# result = subprocess.run(rasa_run, shell=True, capture_output=True, text=True)
# print(result.stdout)


# Load the pre-trained Rasa model
model_path = "SDP/ss23-speech_gesture_comm/mdr_rasa/models/cocktail_party_Regex/models/20230723-173417-glass-captain.tar.gz"
interpreter = Interpreter.load(model_path)


def start_rasa_server():
    subprocess.Popen(["rasa", "run", "--enable-api"])
    # Allow some time for the server to start
    time.sleep(10)

def interact_with_rasa():
    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break

        url = "http://localhost:5005/webhooks/rest/webhook"
        data = {"sender": "user", "message": message}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            responses = response.json()
            for r in responses:
                print(f"Bot: {r['text']}")
        else:
            print("Failed to get a response from the Rasa server.")

if __name__ == "__main__":
    start_rasa_server()
    print("Bot: Type 'exit' to end the conversation.")
    interact_with_rasa()