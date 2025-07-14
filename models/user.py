from pydantic import BaseModel


class User(BaseModel):
    user_info: dict
    access_token: str
    refresh_token: str
    user_data: dict
