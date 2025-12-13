# Description
This is application hosts a simple web server using uvicorn/fastAPI.

The webserver provides the following endpoints:
- /sentencize 
  - Takes in a JSON payload with a "body" required argument.
  - Sentencizes your text using Spacy and returns a list of sentences.



# Build

docker build -f Test.Dockerfile -t test-runner .
docker build -t spacy-app .

# Acceptance Test
docker run -d  --name spacy-app  -p 8980:8980   spacy-app
docker run --rm -it --network container:spacy-app --pid container:spacy-app --cap-add=NET_ADMIN --cap-add=NET_RAW test-runner

# Unit Test
python -m unittest discover -s tests/unit

# Project coding standards:

### Enforced Schemas
- Uses Pydantic to enforce response/request formats.

### Hexagonal Architecture
- Web server implemented via ports + adapters pattern.

### Event Driven Design
- Contains an HTTP client that waits for the webserver's socket listener on 8980 and then initiates connection. 