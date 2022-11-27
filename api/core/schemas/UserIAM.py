from pydantic import BaseModel


class UserIAMGeneral(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "joao",
            }
        }


class UserIAMDB(UserIAMGeneral):
    id: str
