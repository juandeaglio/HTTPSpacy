from fastapi import APIRouter


class MessageRoutes:
    def __init__(self, get_message_uc=None):
        self.router = APIRouter()
        self.uc = get_message_uc
        self.router.add_api_route("/sentencize", self.get, methods=["GET"])

    def get(self):
        return {"message": self.uc.execute()}