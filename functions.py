import json
import requests
import os
from openai import OpenAI
from prompts import instructions

openai_api_key = os.environ['openai_api_key']

client = OpenAI(api_key=openai_api_key)


def example_create_assistant(client):
  file = 'Assistants/example.json'

  if os.path.exists(file):
    with open(file, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID")
  else:
    created_file = client.files.create(file=open("Files/example_file.pdf", "rb"), purpose="assistants")
    assistant = client.beta.assistants.create(
        instructions=instructions, model="gpt-3.5-turbo-1106", tools=[{"type": "retrieval"}], file_ids=[created_file.id])

    with open(file, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print('Created a new assistant and saved the ID')

    assistant_id = assistant.id

  return assistant_id
