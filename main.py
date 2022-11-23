from fastapi import FastAPI

import user

app = FastAPI()

app.include_router(user.router, prefix="/user")