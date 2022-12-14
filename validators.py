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


class NotesValidator(BaseModel):
    id: int|None
    title: str
    description: str
    user_id: int|None


class AddCollaborator(BaseModel):
    id: int|None
    user_id: list[int]
    note_id: int


class RemoveCollaborator(BaseModel):
    note_id: int
    collaborator: list[int]


class LabelValidator(BaseModel):
    id: int|None
    title: str
    color: str


class LabelNotesValidator(BaseModel):
    note_id: int
    label_id: list[int]