# Text to Audiobook
Convert any text to an audiobook, using Azure Cognitive services and Koel.

## Setup:
`docker build -t text-to-audiobook .`

## Run:
`docker run -p 5000:5000 text-to-audiobook`

## Usage:
1) Upload a file to `localhost:5000/convert`
2) After waiting a moment, open your browswer to `localhost:5000/listen/your-book-name`, where "your-book-name" is the name of your file without the extension
