# src/adapters/web/app.py
import uvicorn
from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI()
