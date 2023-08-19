import json

class Memory:
    '''
    @ Rounak Paul \n
    Memory management class for LLM wrapper
    '''
    
    ########################################################
    def __init__(self, history:dict, file_path=None, DEBUG=True):
        '''
        class init\n
        Input:\n
        history:    Dict object containing previous messages\n
        file_path:  File Path where to dump the current memory, 
                    this is optional but it helps to explore 
                    the functionalities and have a cool little 
                    memory effect\n
        DEBUG:      set debug print msg True/False\n
        '''
        self.DEBUG = DEBUG
        self.history = history
        
    ########################################################
    def _dict_to_list(self) -> list:
        '''
        Method to make a list from history dict, to be used as prompt\n
        '''
        temp_list = []
        for key in self.history:
            if key != 'history':
                temp_list.append(f'{key}: {self.history[key]}')
            try:
                temp_list.append(f"history: {self.history['history']}") # This is done to make sure the history stays at the end of the prompt
            except: pass
        return temp_list
        
    ########################################################
    def set(self, key:str, msg:str):
        '''
        Method to set new data to history\n
        Input:\n
        key:    Key in the history dict
        msg:    Value for the given key, updates History
        '''
        msg = msg + '\n'
        if self.DEBUG: print(f'[DEBUG] {key}: {msg}')
        if key == 'history':
            try: self.history[key] += msg # Update history
            except: self.history[key] = msg
        else:
            self.history[key] = msg
        with open('history.json', 'w') as f: # dump current history to a file for later use
            json.dump(self.history,f)
        if self.DEBUG: print('[DEBUG] Updated file')
        
    ########################################################
    def token_overflow(self):
        '''
        method to handle token overflow
        removes oldest message from history whenever called
        can be called multiplt times in a same loop for removing multiple history inputs
        '''
        temp_hist = self.history['history'].split('\n')[:-1]
        self.history['history'] = '\n'.join(temp_hist[1:])
        
    ########################################################
    def get(self):
        '''
        Method to return current history as a string to be used as prompt
        '''
        if self.DEBUG: print(f'[DEBUG] {self.history}')
        temp_list = self._dict_to_list()
        return '\n'.join(temp_list)