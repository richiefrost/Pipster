# Pipster - Text to audiobook
Convert any text to an audiobook and listen to it from your browser, using Azure Cognitive services.

# How it works
Upload any text file and Pipster takes care of the rest. You'll get a link to listen to the audiobook after it's been processed. Since this link is in MP3 format, you can even use it to stream to your own application, like an iOS app.

#### Note:
If you're developing on Windows, it's highly recommended to use the Docker image, since the paths and dependencies used are in Unix format.

## Prerequisites:
1) An Azure Cognitize Services (Speech Services) instance. You can get one <a href="https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/" target="_blank">here</a>
2) Copy `config-example.json` to `config.json` and fill in your own values:
    - `subscription-key`: Also known as "KEY 1" from your Cognitive Services resource's Keys page
    - `resource-region`: The region where your Cognitive Services Text to Speech instance lives, i.e. westus2

## Setup:
`docker build -t pipster .`

## Run:
`docker run -p 5000:5000 pipster`

## Usage:
1) Upload a file to `localhost:5000/convert`
2) After waiting a moment, open your browswer to `localhost:5000/listen/your-book-name`, where "your-book-name" is the name of your file without the extension
