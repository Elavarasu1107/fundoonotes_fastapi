import json
from fastapi import FastAPI, Request, Response
from utils import ApiException, logger
import labels
import notes
import user

app = FastAPI()
@app.middleware('http')
async def exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except ApiException as ex:
        logger.exception(str(ex))
        response =  Response(content=json.dumps({'message': str(ex.message), 'status': ex.status}),
                             status_code=400,
                             media_type='application/json')
    except Exception as ex:
        logger.exception(str(ex))
        response =  Response(content=json.dumps({'message': str(ex), 'status': 400}),
                             status_code=400,
                             media_type='application/json')
    return response


app.include_router(user.router, prefix="/user")
app.include_router(notes.router, prefix="/notes")
app.include_router(labels.router, prefix="/labels")