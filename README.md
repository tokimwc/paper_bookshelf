## Language

- [日本語](./README_JP.md)


# Paper Bookshelf for Mattermost


This Python script is an automation tool designed to search for the latest papers from arXiv based on specified keywords, generate summaries of those papers, and then post those summaries to a Mattermost channel. It focuses particularly on the field of computer science, including artificial intelligence, machine learning, and robotics.

## Features

- Searches arXiv for the latest papers related to specified keywords.
- Generates summaries of the papers.
- Automatically posts the summaries to a Mattermost channel.

## Prerequisites

1. Set the URL of your Mattermost server, the access token for your bot, and the ID of the channel you want to post to as environment variables.
2. Install the required dependencies.

### Environment Variables

Please set the following environment variables:

- `YOUR_MATTERMOST_URL`: The URL of your Mattermost server.
- `YOUR_BOT_ACCESS_TOKEN`: The access token for your Mattermost bot.
- `YOUR_CHANNEL_ID`: The ID of the channel where you want to post.

### Setting up Your Environment

1. Install [Python](https://www.python.org/downloads/).
2. Clone or download this repository.
3. Run `pip install -r requirements.txt` to install the required packages.

## How to Use

1. Set the necessary environment variables in a `.env` file.
2. Execute the script.

```sh
python paper_letter_lm.py
```
## Script Structure
- 'main()': The main execution function. Calls the job() function for each keyword based on the keyword list.
- job(keyword, paper_hash, is_debug): Searches arXiv for papers based on the specified keyword and posts their summaries to Mattermost.
- get_summary(result): Generates a summary from the arXiv search results.
- post_to_mattermost(mattermost_channel_id, message): Posts a message to the specified Mattermost channel.

## Notes
- Instead of using the OpenAI API directly, this script utilizes LM Studio's AI tool capabilities to run LLMs via an HTTP server feature. This allows for the operation of language models directly on a local server, supporting entirely offline functionality.
- For actual deployment, LM Studio facilitates the use of models through its in-app Chat UI or an OpenAI compatible local server. You can download any compatible model files from HuggingFace repositories and explore new & noteworthy LLMs directly from the app's homepage.

For more information on LM Studio, please visit [LM Studio](https://lmstudio.ai/).

