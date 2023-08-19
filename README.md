# Project: Implementing LLM Wrapper from scratch. The wrapper should be able to:

### 1) The LLM wrapper should be able to handle the rate limit errors and token limit error. It should pipeline the data again to the LLM. 

### 2)The LLM wrapper should implement a sequence of the current conversation, with the user inputs, prompts and history.

### 3)The LLM wrapper should be able to maintain the history of the conversation in accordance with the token limit and format the prompt accordingly. 

### 4)The prompt that’s being passed to the LLM wrapper should be formatted at every step of the conversation with as many as input variable we require. (For example if the prompt currently consists of 3 variables, the variable’s of the prompt must be updated before or after a call is made to the LLM while maintaining the history of the conversation.)

Note - Make this model from scratch do not use langchain. 

---
---

This project is a wrapper for LLM models [Currently supports only OpenAI API]

Install required python(3.7+) modules:
```
python -m venv venv
pip install -r requirements.txt
```
Set your OpenAI api key in ```api_keys.py```

Activate the Virtual Env and
Run using the following command:
```
python main.py
```
### Class:
LLM
```
Methods:
    _get_response
    update_prompt_variables
    get
```
Memory
```
Methods:
    _dict_to_list
    set
    token_overflow
    get
```



