from fastapi import FastAPI

import labels
import notes
import user

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(notes.router, prefix="/notes")
app.include_router(labels.router, prefix="/labels")