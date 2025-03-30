# LLM CRUD Application

A Slack bot that uses OpenAI's language models to interpret natural language messages and perform CRUD operations on a user database.

## Features

- Natural language processing to interpret user intents
- Supports Create, Read, Update, and Delete operations
- Integration with Slack for messaging interface
- MySQL database for persistent storage

## Setup

### Prerequisites

- Python 3.8+
- MySQL database
- Slack workspace with admin permissions
- OpenAI API key

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

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
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

## Project Structure

- `main.py`: Slack bot application entry point
- `llm.py`: LLM integration for message interpretation
- `db.py`: Database connection and CRUD operations
- `action_config.yaml`: Configuration for supported actions and parameters
- `schema.sql`: Database schema definition

## How It Works

1. The Slack bot receives a message
2. The message is sent to the `MessageInterpreter` which:
   - Classifies the intent (CREATE, READ, UPDATE, DELETE)
   - Extracts relevant parameters (email_id, first_name, last_name)
3. The extracted information is passed to the `UserManager` to execute the database operation
4. The result is sent back to the user in Slack

