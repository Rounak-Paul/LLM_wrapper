from LLM_wrapper import LLM

import api_keys

# LLM Setup
api_key = api_keys.OPEN_AI
LLM = LLM.LLM(api_key=api_key)

prompt = "Human: The secret key is apple\nAI: Ok, apple\nHuman: what is the secret key?"


response = LLM.get(prompt)
print(response)
