from fastapi import APIRouter, Request, Response, status

from models import User
from utils import JWT, TokenRole, logger
from validators import UserLoginValidator, UserValidator

router = APIRouter()

@router.post("/register/")
def user_register(payload: UserValidator, response: Response):
    """
    This function registers user to the database
    """
    try:
        user = User.objects.create(**payload.dict())
        return user.to_dict()
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex), "status": 400, "data": {}}


@router.post("/login/")
def user_login(payload: UserLoginValidator, response: Response):
    try:
        user = User.objects.get_or_none(**payload.dict())
        if user:
            token = JWT().encode({"user_id": user.id, "role": TokenRole.auth.value})
            return {"message": "Login Successful", "data": token}
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"message": "Invalid Credentials"}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": str(ex)}