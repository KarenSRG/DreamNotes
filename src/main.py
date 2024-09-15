from fastapi import FastAPI

from src.note import router as note_router
from src.user import router as user_router

app = FastAPI()

app.include_router(note_router, prefix="/api/notes", tags=["notes"])
app.include_router(user_router, prefix="/api/user", tags=["user"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the DreamNotesAPI."}
