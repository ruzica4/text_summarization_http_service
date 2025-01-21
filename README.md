# HTTP REST API Service To Summarize Large English Sentences

## Introduction
This HTTP service provides a feature to summarize long English text. Users can send text to an endpoint, receive a unique document ID where the summarization is saved in the database, and retrieve the summarized version of the text using the same ID.

## Getting Started
To run the service:

1. Navigate to the `text_summarization_http_service` directory.
2. Start the application using the following command:
   ```bash
   docker compose up (-d)
   ```
3. Once the application is running, access the available endpoints and their documentation by visiting:
   ```bash
   http://localhost:5000/swagger
   ```
4. Once done with work, you can close the application(all the services) by running docker compose down, but make sure to be positioned, again, in the `text_summarization_http_service` directory.
5. In order not to see errors regarding imports, you could create a virtual environment, activate it and run pip install:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements3.txt
   ```
   but you don't need it in case running the app using docker.
## Environments

Currently, there are two available environments to choose between (testing should be implemented):
- development
- testing


## Additional considerations
- add logging through the whole app (added partially)
- input sanitization
- available content types
- add hash in case the texts repeats frequently, otherwise not
- add similarity search using vectors if needed
- add testing (which is not working properly right now)
- optimize summarization when we have a very large text as input(maybe use GPU, parallelization, multi-core processing, etc.)

## Text summarization 
Used the code from `https://github.com/LunaticPrakash/Text-Summarization` as a reference
