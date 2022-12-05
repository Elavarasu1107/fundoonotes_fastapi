from fastapi import APIRouter, Depends, Request, Response, status

from models import Collaborator, Notes, User
from utils import logger, verify_user
from validators import AddCollaborator, IdValidator, NotesValidator, RemoveCollaborator

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
        note_list = [note.to_dict() for note in notes]
        collaborators = Collaborator.objects.filter(user_id=user.id)
        for collaborator in collaborators:
            note = Notes.objects.get(id=collaborator.note_id)
            note_list.append(note.to_dict())
        return note_list
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
def delete_note(payload: IdValidator, response: Response, user: User=Depends(verify_user)):
    try:
        Notes.objects.delete(id=payload.id, user_id=user.id)
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.post("/add_collaborator/", status_code=status.HTTP_201_CREATED)
def add_collaborator(payload: AddCollaborator, response: Response, user: User=Depends(verify_user)):
    try:
        note = Notes.objects.get(id=payload.note_id, user_id=user.id)
        for user_id in payload.user_id:
            if user_id != user.id:
                collaborator = User.objects.get(id=user_id)
                note.users.append(collaborator)
        note.objects.save()
        return {"message": "Collaborator Added"}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.delete("/delete_collaborator/", status_code=status.HTTP_204_NO_CONTENT)
def add_collaborator(payload: RemoveCollaborator, response: Response, user: User=Depends(verify_user)):
    try:
        note = Notes.objects.get(id=payload.note_id, user_id=user.id)
        for user_id in payload.collaborator:
            collaborator = User.objects.get(id=user_id)
            note.users.remove(collaborator)
        note.objects.save()
        return {"message": "Collaborator Deleted"}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}