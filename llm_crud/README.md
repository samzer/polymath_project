# LLM CRUD Application

A Slack bot that uses language models to interpret natural language messages and perform CRUD operations on a user database. Supports both OpenAI and Ollama models.

## Features

- Natural language processing to interpret user intents
- Supports Create, Read, Update, and Delete operations
- Integration with Slack for messaging interface
- MySQL database for persistent storage
- Multi-LLM support: OpenAI and Ollama (gemma3)

## Setup

### Prerequisites

- Python 3.8+
- MySQL database
- Slack workspace with admin permissions
- OpenAI API key (if using OpenAI models)
- Ollama (if using local models like gemma3)

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# MySQL Configuration
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_database_name

# Slack Configuration
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_APP_TOKEN=your_slack_app_token

# LLM Provider Configuration
LLM_PROVIDER=openai  # or "ollama"
LLM_MODEL=gpt-4o-mini  # or "gemma3" if using Ollama

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key

# Ollama Configuration (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434  # Optional, defaults to this value
```

### Database Setup

Run the schema.sql file to create the necessary tables:

```bash
mysql -u your_username -p your_database < schema.sql
```

### Installation

```bash
# Clone the repository
cd llm_crud

# Install dependencies
pip install -r requirements.txt
```

For Ollama support, you'll need to install the Ollama Python client and have Ollama running locally:

```bash
pip install ollama
```

Make sure you have the required model pulled in Ollama:

```bash
ollama pull gemma3
```

## Usage

1. Start the application:

```bash
python main.py
```

2. In Slack, mention the bot with a command:

- To create a user: "@bot Add a user with email john.doe@example.com whose name is John Doe"
- To read user information: "@bot Get the details for user with email john.doe@example.com"
- To update a user: "@bot Update John Doe's last name to Smith with email john.doe@example.com"
- To delete a user: "@bot Delete the user with email john.doe@example.com"

## LLM Provider Options

This application supports multiple LLM providers:

1. **OpenAI** (default) - Cloud-based models, requires an API key
   - Set `LLM_PROVIDER=openai` and `LLM_MODEL=gpt-4o-mini` (or another OpenAI model)

2. **Ollama** - Local LLM deployment, no API key required
   - Set `LLM_PROVIDER=ollama` and `LLM_MODEL=gemma3` (or another Ollama model)
   - Ensure Ollama is running and the model is pulled

## Project Structure

- `main.py`: Slack bot application entry point
- `llm.py`: LLM integration for message interpretation and multi-provider support
- `db.py`: Database connection and CRUD operations
- `action_config.yaml`: Configuration for supported actions and parameters
- `schema.sql`: Database schema definition

## How It Works

1. The Slack bot receives a message
2. The message is sent to the `MessageInterpreter` which:
   - Classifies the intent (CREATE, READ, UPDATE, DELETE) using the configured LLM
   - Extracts relevant parameters (email_id, first_name, last_name)
3. The extracted information is passed to the `UserManager` to execute the database operation
4. The result is sent back to the user in Slack
