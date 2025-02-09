# Running the Backend App of the Chat
This backend is a Quart-based web server that provides endpoints for extracting repository data and chating with the repository data.

## Prerequisites
- Ensure you have Python 3.6 or later installed. You can check your Python version by running:

    ```bash
        python --version
    ```

- You also need to install the necessary Python packages. You can do this by running:

    ```bash
        pip install -r requirements.txt
    ```

## Running the Server
To start the server, navigate to the directory containing `main.py` and run:

```bash
    python main.py
```

The server will start and listen for incoming connections.

## Note
Before running the server, navigate to `repo.py` and replace the token with your GitHub token in the `form_metadata` function.


# Running the User Interface of the Chatbot

This document provides a step-by-step guide on how to run and interact the with the chatbot through the user interface.

## Prerequisites

- Node.js and npm (Node Package Manager) installed on your machine. You can download and install them from the official website: [https://nodejs.org/](https://nodejs.org/)

## Steps to Run the Chatbot

1. **Navigate to the project directory**. Open your terminal and navigate to the project directory using the `cd` command. For example:

    ```bash
    cd path/to/local_directory/chatbot_v2.0
    ```

2. **Install the project dependencies**. In the project directory, run the following command to install the necessary dependencies:

    ```bash
    npm install
    ```

3. **Start the project**. After the dependencies are installed, you can start the project with the following command:

    ```bash
    npm start
    ```

    This command starts the development server and the chatbot will be accessible at `http://localhost:3000` in your web browser.

## Stopping the Chatbott

To stop the running Chatbot, press `Ctrl + C` in the terminal where the project is running.

## Note

The Chatbot makes a POST request to the backend through the API at `http://127.0.0.1:5000/extract` to extract repository information and  `http://127.0.0.1:5000/lang-chat-sources` to chat with a your OPENAI token for authorization. Ensure the API is running and the OPENAI token is valid.


# Automating the Process of Getting the Responses and Documents of the Questions.
## Prerequisites
- Ensure you have Python 3.6 or later installed. You can check your Python version by running:

    ```bash
        python --version
    ```

- You also need to install the necessary Python packages. You can do this by running:

    ```bash
        pip install -r requirements.txt
    ```
## Running the Server
To run the script automating the process for all 150 questions, navigate to the directory of the scripts and run:

```bash
    python script/automating_script.py
```

## Note
Before running the script, navigate to `repo.py` and replace the token with your GitHub token in the `form_metadata` function.
