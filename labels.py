from fastapi import APIRouter, Depends, Request, Response, status

from models import Labels, Notes, User
from utils import logger, verify_user
from validators import IdValidator, LabelNotesValidator, LabelValidator

router = APIRouter()

@router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_label(payload: LabelValidator, response: Response, user: User=Depends(verify_user)):
    try:
        label = Labels.objects.create(**payload.dict())
        return label.to_dict()
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.get("/get/", status_code=status.HTTP_200_OK)
def get_label(response: Response, user: User=Depends(verify_user)):
    try:
        labels = Labels.objects.all()
        label_list = [label.to_dict() for label in labels]
        return label_list
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.put("/update/", status_code=status.HTTP_201_CREATED)
def update_label(payload: LabelValidator, response: Response, user: User=Depends(verify_user)):
    try:
        label = Labels.objects.get(id=payload.id)
        label.objects.update(**payload.dict())
        return label.to_dict()
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(payload: IdValidator, response: Response, user: User=Depends(verify_user)):
    try:
        Labels.objects.delete(id=payload.id)
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.post("/add_labelnote/", status_code=status.HTTP_201_CREATED)
def add_label_to_note(payload: LabelNotesValidator, response: Response, user: User=Depends(verify_user)):
    try:
        note = Notes.objects.get(id=payload.note_id, user_id=user.id)
        for label in payload.label_id:
            label = Labels.objects.get(id=label)
            note.labels.append(label)
        note.objects.save()
        return {"message": "Label added to Note"}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}

@router.delete("/delete_labelnote/", status_code=status.HTTP_204_NO_CONTENT)
def delete_label_to_note(payload: LabelNotesValidator, response: Response, user: User=Depends(verify_user)):
    try:
        note = Notes.objects.get(id=payload.note_id, user_id=user.id)
        for label in payload.label_id:
            label = Labels.objects.get(id=label)
            note.labels.remove(label)
        note.objects.save()
        return {"message": "Collaborator Deleted"}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}
