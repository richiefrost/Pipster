# Pipster - Text to audiobook
Convert any text to an audiobook and listen to it from your browser, using Azure Cognitive services.

# How it works
Upload any text file and Pipster takes care of the rest. You'll get a link to listen to the audiobook after it's been processed. Since this link is in MP3 format, you can even use it to stream to your own application, like an iOS app.

#### Note:
If you're developing on Windows, it's highly recommended to use the Docker image, since the paths and dependencies used are in Unix format.

Prerequisites:
1) An Azure Cognitize Services (Speech Services) instance. You can get one [here](https://portal.azure.com)
2) Copy `config-example.json` to `config.json` and fill in your own values:
    - `subscription-key`: Also known as "KEY 1" from your Cognitive Services resource's Keys page
    - `token-url`: Available under "Quick Start, step 2b" from your Cognitive Services resource's Quick Start page
    - `api-url`: The URL to which text to speech requests will be sent. This depends on your resource's region, and you can find a list of valid values <a href="https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech#standard-and-neural-voices" target="_blank">here</a>

## Setup:
`docker build -t pipster .`

## Run:
`docker run -p 5000:5000 pipster`

## Usage:
1) Upload a file to `localhost:5000/convert`
2) After waiting a moment, open your browswer to `localhost:5000/listen/your-book-name`, where "your-book-name" is the name of your file without the extension
