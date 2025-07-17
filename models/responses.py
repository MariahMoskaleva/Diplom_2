from typing import List, Dict

from pydantic import BaseModel, Field


class UserData(BaseModel):
    email: str
    name: str


class CreateUserNotSuccessResponse(BaseModel):
    success: bool
    message: str


class LoginSuccessResponse(BaseModel):
    success: bool
    accessToken: str
    refreshToken: str
    user: dict


class LoginNotSuccessResponse(BaseModel):
    success: bool
    message: str


class UpdateUserSuccessResponse(BaseModel):
    success: bool
    user: UserData


class UpdateUserUnauthorizedResponse(BaseModel):
    success: bool
    message: str


class CreateOrderSuccessResponse(BaseModel):
    success: bool
    name: str
    order: Dict


class CreateOrderErrorResponse(BaseModel):
    success: bool
    message: str


class Ingredient(BaseModel):
    id: str = Field(alias="_id")
    name: str
    type: str


class IngredientsResponse(BaseModel):
    success: bool
    data: List[Ingredient]