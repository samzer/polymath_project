import os
import yaml
import json
from openai import OpenAI
from ollama import chat
from typing import Optional, Union, Dict, Any
from dotenv import load_dotenv
from db import UserManager

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_ollama_completion(
    prompt: str,
    system_message: str = None,
    model: str = "gemma3",
    temperature: float = 0.7
) -> str:
    try:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        response = chat(
            model=model,
            messages=messages,
            options={"temperature": temperature}
        )
        
        return response.message.content.strip()

    except Exception as e:
        raise Exception(f"Error calling Ollama API: {str(e)}")

def get_openai_completion(
    prompt: str,
    system_message: str = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> str:
    try:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}")

def get_completion(
    prompt: str,
    system_message: str = None,
    provider: str = "openai",
    model: str = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> str:
    """Unified interface for getting completions from different LLM providers"""
    if provider == "openai":
        model = model or "gpt-4o-mini"
        return get_openai_completion(prompt, system_message, model, temperature, max_tokens)
    elif provider == "ollama":
        model = model or "gemma3"
        return get_ollama_completion(prompt, system_message, model, temperature)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

class MessageInterpreter:
    def __init__(self, provider="openai", model=None):
        # Read the yaml file
        self.user_manager = UserManager()
        self.provider = provider
        self.model = model
        with open('action_config.yaml', 'r') as file:
            self.action_config = yaml.safe_load(file)
        
    def classify_message_action(self, message: str) -> str:
        # Get the action names from the action config
        action_names = [action['name'] for action in self.action_config['actions']]

        # Create the context prompt
        context_prompt = f"""You are an interpreter that interprets an action based on the message received after. 
Following is a configuration of action and based on the message, interpret which action should be taken and the output is the name of the action 
{action_names}
"""
        return get_completion(message, system_message=context_prompt, provider=self.provider, model=self.model)
    
    def get_action_parameters(self, action_name: str) -> dict:
        # Find the action in the list by matching the name
        for action in self.action_config['actions']:
            if action['name'] == action_name:
                return action['parameters']
        raise ValueError(f"Action '{action_name}' not found in configuration")

    def extract_message_parameters(self, message: str, parameters: dict) -> dict:
        # Create the context prompt
        context_prompt = f"""You are an interpreter that extracts parameters from the message. 
Following is a configuration of the parameters, extract out the parameters from the message
return it in a json format with the parameter name as the key and the value as the value from the message.
Don't use code blocks or any other formatting.
{parameters}
"""

        # Get the response from the LLM
        response = get_completion(message, system_message=context_prompt, provider=self.provider, model=self.model)

        return response

    def invoke(self, message: str) -> dict:
        # Classify the message
        action_name = self.classify_message_action(message)

        # Get the parameters
        action_parameters = self.get_action_parameters(action_name)

        # Extract the parameters from the message
        parameters = self.extract_message_parameters(message, action_parameters)
        parameters = json.loads(parameters)
        
        # Call the user manager method based on the action name
        self.user_manager.execute_action(action_name, parameters)

        return {
            "action_name": action_name,
            "parameters": parameters
        }


# Example usage:
if __name__ == "__main__":
    message_interpreter = MessageInterpreter()
    result = message_interpreter.invoke("Add an john@test.com whose name is John Doe")
    print(f"Response: {result}")

    json_result = json.loads(result['parameters'])
    print(json_result)