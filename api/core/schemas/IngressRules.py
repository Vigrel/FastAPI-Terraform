from pydantic import BaseModel


class IngressGeneral(BaseModel):
    description: str
    from_port: int
    to_port: int
    protocol: str
    cidr_blocks: list = ["172.16.0.0/16"]
    ipv6_cidr_blocks: list = []
    prefix_list_ids: list = []
    security_groups: list = []
    self: bool = False

    class Config:
        schema_extra = {
            "example": {
                "description": "For HTTPS",
                "from_port": 443,
                "to_port": 443,
                "protocol": "tcp",
                "cidr_blocks": ["172.16.0.0/16"],
                "ipv6_cidr_blocks": [],
                "prefix_list_ids": [],
                "security_groups": [],
                "self": False,
            }
        }


class IngressDB(IngressGeneral):
    id: str
