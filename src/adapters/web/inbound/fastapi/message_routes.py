from fastapi import APIRouter, Body

from src.application.sentences import Sentences


class MessageRoutes:
    def __init__(self, app: Sentences):
        self.app = app
        self.router = APIRouter()
        self.router.add_api_route("/sentencize", self.sentencize, methods=["POST"])

    def sentencize(self, body: str = Body(..., embed=True)):
        return {"sentences": self.app.break_apart(body)}
