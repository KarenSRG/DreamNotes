from fastapi import FastAPI

from src.note.router import router as note_router
from src.user.router import router as user_router

app = FastAPI()

app.include_router(note_router, prefix="/api", tags=["notes"])
app.include_router(user_router, prefix="/api", tags=["user"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the DreamNotesAPI."}
