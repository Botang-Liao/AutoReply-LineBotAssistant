# Project Name

This is an automatic question-answering LINE bot powered by a local LLM model named Qwen.

## Features

- Automatically responds to questions sent through LINE.
- Runs locally to ensure data security.
- Easy to deploy and maintain.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- LINE Messaging API account
- A local or cloud server setup
## File structure
```
.
├── app                       # application directory
├── config.ini.example        # Example configuration file, used to set up the actual 'config.ini'
├── flaskr                    # Flask application directory
│   ├── api_linebot.py        # Handles the API interactions for the LINE bot
│   ├── __init__.py           # Initializes the Flask application
│   ├── LineBot               # Contains modules specific to LINE bot functionalities
│   │   ├── button_message.py # Handles creation of button messages in LINE bot
│   │   ├── button_template.py# Defines templates for button messages in LINE bot
│   ├── utils.py              # Utility functions used across the Flask application
│   └── VDB_API               # Directory for Vector Database API functionalities
│       ├── abandon_docs      # Directory for unused documents in vector database
│       ├── docs              # Directory for used documents in vector database
│       ├── nttu_llm.py       # LLM model model with vector database
│       ├── utils             # Utility scripts for VDB_API
│       │   ├── config.py     # Configuration settings for VDB_API
│       │   ├── file_processor.py # Handles file processing tasks
│       │   ├── list_all_file_in_a_path.py # Lists all files in a specified directory
│       │   └── transfer_chinese.py # Utility for handling Chinese character transfers
│       └── vectordb_manager.py # Manages interactions with the vector database
├── README.md                 # Markdown file containing project overview and instructions
├── requirements.txt          # Lists dependencies to be installed using pip
└── server.py                 # Main server file to run the Flask application

```
## Installation

Follow these steps to set up your LINE bot:

1. **Obtain LINE API Keys**:
   - Visit the LINE Developers Console, create a Provider and a Channel.
   - Copy your Channel secret and Channel access token.

2. **Build Environment**

    - Clone this repo
        ```
        git clone https://github.com/Botang-Liao/AutoReply-LineBotAssistant.git
        cd AutoReply-LineBotAssistant/
        ```
    - Install the Python dependencies
        ```
        pip3 install -r deployment/requirements.txt
        ```
    - Run the code
        ```
        gunicorn -w 1 -b 0.0.0.0:54089 server:app    
        ```

## Usage

How to interact with your LINE bot:

- Add the LINE bot as a friend.
- Simply type a question into the chat window.
- Wait for the bot to respond.


