# MCP-server
I made a simple MCP server which can support your Moodle manipulation.

this MCP server can assist following thing,
- show the due date of your assignments
- show the unread messages from your moodle
- show the uncompleted quizes
- show all courses you take


## File architecture
- config.json  : register your Moodle URL and its token, also API Key for OpenAI API and model type
- main.py   : the rooting for FastAPI and configuration of templates
- server.py : input/ouput of user via OpenAI API and the control for tools calling 
- tool_registry.py  : store the meta information of tools and its assignments
- tools/
  - moodle_tools.py : functions which call Moodle API(e.g. duedate, new messages) 
- templates/
  - index.html  : UI
- static/
  - style.css
- requirments.txt   : all you need to run 
- README.md


## How to run
1. $ python -m venv venv
2. $ source venv/bin/activate # macOS/Linux
   $ .\venv\Scripts\activate # windows PowerShell
3. $ pip install -r requirements.txt
4. $ python client.py server.py

