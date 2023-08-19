import openai
import time
from tqdm import tqdm

from LLM_wrapper.memory import Memory

class LLM(Memory):
    '''
    @ Rounak Paul \n
    LLM Wrapper
    Currently Supported LLMs: OpenAI
    
    '''
    
    ########################################################
    def __init__(self, api_key:str, history_dict_from_file=None, engine="text-davinci-003", max_tokens=50, DEBUG=True, **kwargs) -> None:
        '''
        class init\n
        Inputs:\n
        api_key:                    OpenAI api key\n
        history_dict_from_file:     pass existing history.json content to this, if not new conversation will start\n
        engine:                     AI engine to use\n
        max_tokens:                 tokens the AI model is expected to generate\n
        DEBUG:                      set debug print msg True/False\n
        **kwargs:                   This is being used to pass prompt variables to the history context\n
        '''
        self.DEBUG = DEBUG
        self.engine = engine
        self.max_tokens = max_tokens
        openai.api_key = api_key
        self.retry_time_s = 10 # in Exception, time in Seconds before re-trying
        self.history = {} # dict object to hold live chat history
        self.history_key = 'history' # key for live chat history
        
        # Load History
        if history_dict_from_file != None:
            if self.DEBUG: print(f'[DEBUG] len of previous history: {len(history_dict_from_file)}')
            for key in history_dict_from_file:
                self.history[key] = history_dict_from_file[key]
        
        # Set prompt parameters
        for key, value in kwargs.items():
            self.history[key] = f'{value}'
        
        # init the memory class
        super().__init__(self.history,DEBUG=DEBUG)
    
    ########################################################
    def update_prompt_variables(self, key: str, msg: str) -> None:
        '''
        Updates the memory of the current conversation\n
        access any variable by its key value and modify\n
        Input:\n
        key:    Key used in memory\n
        msg:    Value for that key in memory
        '''
        super().set(key, msg)
    
    ########################################################
    def _get_response(self, prompt:str):
        '''
        wrapper for OpenAI LLM model\n
        Input:\n
        prompt:     User given prompt
        '''
        try:
            response = openai.Completion.create(
                engine = self.engine,
                prompt = prompt,
                max_tokens = self.max_tokens
            )
            if response.choices:
                output_text = response.choices[0].text.strip()
                return output_text
            else: return -1 # Retry flag
        except openai.error.RateLimitError as err: # Handle Rate limit error
            print(f'[RateLimitError] {err}')
            return -1 # Retry flag
        except openai.error.InvalidRequestError as err: # Handle Token Limit Error
            print(f'[TokenLimitError] {err}')
            super().token_overflow() # Remove oldest message, somewhat like a FIFO, but the FIFO itself is passed, not the out value
            return -1 # Retry flag
        except Exception as err: # Handle other exceptions and send retry flag
            print(f'[Error] {err}')
            return -1 # Retry flag
    
    ########################################################
    def get(self, prompt:str) -> str:
        '''
        get method, returns the LLM response string\n
        Input:\n
        prompt:     User given prompt
        '''
        context = super().get() # load the context from history
        super().set(self.history_key,f'Human: {prompt}') # Update the history with the latest prompt
        prompt = f'{context}\n{prompt}' # make prompt with the context
        while True:
            response = self._get_response(prompt)
            
            # Handle Retry event
            if response == -1: 
                if not self.DEBUG: 
                    continue
                print('[LLM] No response generated.')
                print(f'[LLM] Retrying in {self.retry_time_s}seconds')
                for _ in tqdm(range(self.retry_time_s)):
                    time.sleep(self.retry_time_s/self.retry_time_s)
            else: 
                super().set(self.history_key,f'AI: {response}') # Update the history with the latest AI response
                break
        return response