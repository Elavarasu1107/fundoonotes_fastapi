from pydantic import BaseModel, EmailStr


class IdValidator(BaseModel):
    id: int

class UserValidator(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: int 
    location: str
    is_superuser: bool|None= False


class UserLoginValidator(BaseModel):
    username: str
    password: str
