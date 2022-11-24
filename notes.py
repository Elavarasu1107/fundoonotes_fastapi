from fastapi import APIRouter, Depends, Request, Response, status

from models import Notes, User
from utils import logger, verify_user
from validators import IdValidator, NotesValidator

router = APIRouter()

@router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_note(payload: NotesValidator, response: Response, user: User=Depends(verify_user)):
    try:
        payload.user_id = user.id
        note = Notes.objects.create(**payload.dict())
        return note.to_dict()
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.get("/get/", status_code=status.HTTP_200_OK)
def get_note(response: Response, user: User=Depends(verify_user)):
    try:
        notes = Notes.objects.filter(user_id=user.id)
        return notes
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.put("/update/", status_code=status.HTTP_201_CREATED)
def update_note(payload: NotesValidator, response: Response, user: User=Depends(verify_user)):
    try:
        payload.user_id = user.id
        note = Notes.objects.get(id=payload.id, user_id=payload.id)
        note.objects.update(**payload.dict())
        return note.to_dict()
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def update_note(payload: IdValidator, response: Response, user: User=Depends(verify_user)):
    try:
        Notes.objects.delete(id=payload.id, user_id=user.id)
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}