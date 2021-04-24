Script for delete ALL posts from your VK wall.

RUN:
> pip install -r requirements.txt
> 
> python -m src

Next - follow the messages in terminal.


If you don't trust me - register your own application in VK and overwrite APP_ID in \_\_main__.py.

Why is the program synchronous and slow? 
Because in the VK API, we need to send a request to delete each post on the wall. 
Posting cats and dogs with asyncio - VK begins to suffer and dull (Too many requests).
