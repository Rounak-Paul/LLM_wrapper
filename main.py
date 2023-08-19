from LLM_wrapper import LLM_openai
import json

import api_keys

# LLM Setup
history_file_path = 'history.json'
with open(history_file_path,'r') as f:
    history = json.load(f)
api_key = api_keys.OPEN_AI
LLM = LLM_openai.LLM(
                        DEBUG=True,
                        api_key=api_key,
                        engine="text-davinci-003",
                        history_dict_from_file = history,
                        max_tokens=16,
                        context='Covid safety',
                        audience='kids',
                        behave_like='You are a kid, who is learning'
                    )

while True:
    prompt = input('Human: ')
    response = LLM.get(prompt)
    print(f'AI: {response}')
