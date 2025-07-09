from pydantic import BaseModel


class CreateUserNotSuccessResponse(BaseModel):
    success: bool
    message: str
