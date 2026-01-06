# Stack Overflow Summarizer Discord Bot

A Discord bot that summarizes Stack Overflow questions.

## Features

- Fetches a Stack Overflow question from a URL.
- Summarizes the question and the most relevant answer.
- Displays the summary in a clean, embedded format.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the root of the project and add your Discord bot token:
    ```
    DISCORD_TOKEN=<your-token-here>
    ```

3.  **Install dependencies:**
    Install the required Python libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the bot:**
    ```bash
    python bot.py
    ```

2.  **Use the `!so` command:**
    In a Discord channel where the bot is present, use the `!so` command followed by the URL of the Stack Overflow question you want to summarize:
    ```
    !so https://stackoverflow.com/questions/12345/example-question
    ```

## Configuration

You can change the bot's command prefix by editing the `config.json` file. The default prefix is `!`.
