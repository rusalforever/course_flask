from datetime import date
from pydantic import BaseModel, ConfigDict


class AnimalAge:
    birth_date: date

    @property
    def age(self) -> int:
        today = date.today()
        animal_age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            animal_age -= 1
        return animal_age


class AnimalCreate(BaseModel, AnimalAge):
    animal_type: str
    name: str
    breed: str
    photo_url: str


class AnimalResponse(BaseModel, AnimalAge):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    breed: str
    photo_url: str
    animal_age: int
