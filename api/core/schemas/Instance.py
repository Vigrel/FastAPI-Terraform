from pydantic import BaseModel


class InstanceGeneral(BaseModel):
    ami: str
    instance_type: str

    class Config:
        schema_extra = {
            "example": {
                "ami": "ami-0149b2da6ceec4bb0",
                "instance_type": "t2.micro",
            }
        }


class InstanceDB(InstanceGeneral):
    id: str
