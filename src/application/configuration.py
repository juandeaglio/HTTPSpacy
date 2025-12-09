import uvicorn
from fastapi import FastAPI

from src.adapters.nlp.outbound.sentencizer import SentencizerAdapter
from src.adapters.web.inbound.fastapi.message_routes import MessageRoutes
from src.application.sentences import Sentences


def configure_app(sentences: SentencizerAdapter):
    api = FastAPI()
    sentencizer = Sentences()
    routes = MessageRoutes(app=sentencizer)
    api.include_router(routes.router)
    config = uvicorn.Config(api, host="127.0.0.1", port=80, log_level="warning")
    server = uvicorn.Server(config)
    return server