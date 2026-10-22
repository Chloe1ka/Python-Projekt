from pydantic import BaseModel, ConfigDict


class MitgliedRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vorname: str
    nachname: str
    email: str


class MitgliedCreate(BaseModel):
    vorname: str
    nachname: str
    email: str
