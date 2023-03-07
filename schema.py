from pydantic import BaseModel
from pydantic import validator
from pydantic.utils import GetterDict


from peewee import ModelSelect
from typing import Any


#----------------- SETTING -----------------

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

#----------------- USER -----------------

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 8 or len(username) > 50:
            raise ValueError('Must be 8 to 50 characters.')
        return username 

class UserResponseModel(ResponseModel):
    id: int
    username: str

#----------------- MOVIE -----------------

class MovieRequestModel(BaseModel):
    title: str

    @validator('title')
    def title_validator(cls, title):
        if len(title) > 50:
            raise ValueError('Must be at least 50 characters.')
        return title


class MovieResponseModel(ResponseModel):
    id: int
    title: str

#----------------- REVIEW -----------------

class RatingValidatorModel:
    @validator('rating')
    def rating_validator(cls, rating):
        if rating < 1 or rating > 5:
            raise ValueError('The rating must be between 1 to 5 points.')
        return rating

class ReviewRequestModel(BaseModel, RatingValidatorModel):
    user_id: int
    movie_id: int
    description: str
    rating: int

class ReviewResponseModel(ResponseModel):
    id: int
    description: str
    rating: int

class UpdateReviewModel(BaseModel, RatingValidatorModel):
    description:str
    score:int
    
    