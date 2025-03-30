from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
from llm import MessageInterpreter

# Load environment variables from .env file
load_dotenv()

# Get LLM provider and model from environment variables
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL")

# Initialize app with bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listen for messages in channels the bot is added to
@app.message()
def message_handler(message, say):
    """Handle incoming messages"""
    # Echo the message back (as an example)
    say(f"Processing message: {message['text']}")

# Listen for direct mentions of the bot
@app.event("app_mention")
def handle_mention(event, say):
    """Handle when bot is mentioned"""

    # Initialize message interpreter with configured provider and model
    message_interpreter = MessageInterpreter(provider=LLM_PROVIDER, model=LLM_MODEL)
    
    # Get interpretation result
    try:
        result = message_interpreter.invoke(event['text'])
        
        # Parse the parameters from JSON string
        parameters = result['parameters']
        
        # Format response message
        response = f"Action: {result['action_name']}\nResponse: {parameters}"
        say(response)
        
    except Exception as e:
        say(f"Sorry, I couldn't process that command: {str(e)}")


if __name__ == "__main__":
    # Start your app using Socket Mode
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()