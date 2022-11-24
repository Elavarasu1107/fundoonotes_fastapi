from fastapi import FastAPI

import notes
import user

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(notes.router, prefix="/notes")