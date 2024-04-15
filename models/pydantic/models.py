from datetime import date, timedelta
from pydantic import BaseModel, ConfigDict, computed_field
from datetime import date


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


    @computed_field
    @property
    def age(self) -> int:
        return date.today().year - self.birth_date.year


