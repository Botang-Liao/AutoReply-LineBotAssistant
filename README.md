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


