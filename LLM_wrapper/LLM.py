import openai
import time
from tqdm import tqdm

class LLM:
    def __init__(self, api_key:str, engine="text-davinci-003", max_tokens=50, DEBUG=True) -> None:
        self.DEBUG = DEBUG
        self.engine = engine
        self.max_tokens = max_tokens
        openai.api_key = api_key
        self.retry_time_s = 10
    
    def _get_response(self, prompt:str):
        try:
            response = openai.Completion.create(
                engine = self.engine,
                prompt = prompt,
                max_tokens = self.max_tokens
            )
            if response.choices:
                output_text = response.choices[0].text.strip()
                return output_text
            else: return -1
        except openai.error.RateLimitError as err:
            print(f'[RateLimitError] {err}')
            return -1
        except openai.error.InvalidRequestError as err:
            print(f'[TokenLimitError] {err}')
            return -1
    
    def get(self, prompt:str) -> str:
        context = '\n'
        prompt = f'{context}\n{prompt}'
        while True:
            response = self._get_response(prompt)
            if response == -1:
                if self.DEBUG: 
                    print('[LLM] No response generated.')
                    print(f'[LLM] Retrying in {self.retry_time_s}seconds')
                    for _ in tqdm(range(self.retry_time_s)):
                        time.sleep(self.retry_time_s/self.retry_time_s)
            else: break
        return response
        