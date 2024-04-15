from datetime import date
from pydantic import BaseModel, ConfigDict


class AnimalCreate(BaseModel):
    animal_type: str
    name: str
    birth_date: date
    breed: str
    photo_url: str


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    birth_date: date
    breed: str
    photo_url: str
