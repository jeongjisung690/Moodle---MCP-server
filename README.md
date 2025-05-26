# MCP-server
I made a simple MCP server which can support your Moodle manipulation.
You can use LLM models which are "OpenAI" and localLLM(ollama).

this MCP server can assist following thing,
- show the due date of your assignments
- show the unread messages from your moodle
- show the uncompleted quizes
- show all courses you take


## File architecture
- .env : your environment settings
- client.py   : process user's query, create a answer via LLM
- client_localLLM.py   : when using a local LLM(ollama) 
- server.py : run tools
- requirments.txt  
- README.md


## How to run
firstly, please input your information in .env file.
```
1. $ python -m venv venv
2. $ source venv/bin/activate # macOS/Linux
   $ .\venv\Scripts\activate # windows PowerShell
3. $ pip install -r requirements.txt
4. $ python client.py server.py # when using OpenAI
     ($ python client_localLLM.py server.py # when using ollama model)
```

