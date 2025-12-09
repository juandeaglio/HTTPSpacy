import uvicorn
from fastapi import FastAPI

from src.adapters.web.inbound.fastapi.message_routes import MessageRoutes
from src.application.sentences import Sentences
from src.ports.nlp.outbound.sentencizing import SentencizerPort


def configure_app(sentencizer: SentencizerPort) -> uvicorn.Server:
    api = FastAPI()
    sentences = Sentences(sentencizer)
    routes = MessageRoutes(app=sentences)
    api.include_router(routes.router)
    config = uvicorn.Config(api, host="127.0.0.1", port=80, log_level="warning")
    server = uvicorn.Server(config)
    return server
