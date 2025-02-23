from fastapi import FastAPI

from tracker.service import get_tracker

app = FastAPI()
tracker = get_tracker()
