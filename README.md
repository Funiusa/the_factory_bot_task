# The Factory bot task
## Description

#### Using Flask, FastAPI or Django and Django REST Framework, write an API for receiving messages and sending them to a Telegram bot
#### The functionality of the finished task should look like this:

> We receive a message through the API, then we send it to the Telegram bot.

### Scheme of work:

 - User registers in our system. When registering, it specifies the
    login, password and name
   
 - The user finds a bot in Telegram and subscribes to it. At this stage, you need to create a Telegram bot.
 - Generates a token in his personal account and binds this token to his chat. 
    A simple way of implementation: the bot remembers any incoming message from the user as a user token
 - The user sends his message to the API. At this moment, the bot immediately duplicates it in Telegram. 
 The user should only receive his own messages. 

**Message format:** 

	{Username}, I got a message from you:
	{Message} 

*The message should start from a new line.*

### Functionality:
 - Authorization
 - Registration
 - Generating a token for a telegram bot. (Only after authorization)
 - Sending messages to your bot. 
 On the server to fix: the date and body of the message. (Only after authorization)
 - Getting a list of all messages: date of sending, message (Only after authorization)
 
*The functionality above should work via the REST API.*
