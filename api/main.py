import json
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status

from api.core.models import db
from api.core.schemas import IngressRules, Instance, UserIAM

app = FastAPI()
# os.system("terraform init")


@app.get(
    "/instances/",
    response_model=list[Instance.InstanceDB],
    status_code=status.HTTP_200_OK,
    tags=["Intances"],
    summary="Get all method",
    description="Return all instances in database",
)
async def get_instances() -> list[Instance.InstanceDB]:
    return db.instances


@app.post(
    "/instances/",
    response_model=Instance.InstanceDB,
    status_code=status.HTTP_201_CREATED,
    tags=["Intances"],
    summary="Create method",
    description="Create an instance based on it's infos and add a random uuid4 id",
)
async def add_instance(instance: Instance.InstanceGeneral) -> Instance.InstanceDB:
    instance_dict = instance.dict()
    instance_dict["id"] = str(uuid4())
    db.instances.append(Instance.InstanceDB(**instance_dict))
    return db.instances[-1]


@app.delete(
    "/instances/{instance_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Intances"],
    summary="Delete one method",
    description="Delete an instance by it's ID",
)
async def delete_instance(instance_id: str) -> dict[str]:
    for instance in db.instances:
        if instance.id == instance_id:
            db.instances.remove(instance)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Instance not found"
    )


@app.get(
    "/ingress/",
    response_model=list[IngressRules.IngressDB],
    status_code=status.HTTP_200_OK,
    tags=["IngressRules"],
    summary="Get all method",
    description="Return all IngressRules in database",
)
async def get_ingress() -> list[IngressRules.IngressDB]:
    return db.ingress


@app.post(
    "/ingress/",
    response_model=IngressRules.IngressDB,
    status_code=status.HTTP_201_CREATED,
    tags=["IngressRules"],
    summary="Create method",
    description="Create an IngressRules based on it's infos and add a random uuid4 id",
)
async def add_ingress(ingress: IngressRules.IngressGeneral) -> IngressRules.IngressDB:
    ingress_dict = ingress.dict()
    ingress_dict["id"] = str(uuid4())
    db.ingress.append(IngressRules.IngressDB(**ingress_dict))
    return db.ingress[-1]


@app.delete(
    "/ingress/{rule_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["IngressRules"],
    summary="Delete one method",
    description="Delete an IngressRules by it's ID",
)
async def delete_ingress_rule(rule_id: str) -> dict[str]:
    for rule in db.ingress:
        if rule.id == rule_id:
            db.ingress.remove(rule)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")


@app.get(
    "/users/",
    response_model=list[UserIAM.UserIAMDB],
    status_code=status.HTTP_200_OK,
    tags=["IAM Users"],
    summary="Get all method",
    description="Return all users in database",
)
async def get_users() -> list[UserIAM.UserIAMDB]:
    return db.users


@app.post(
    "/users/",
    response_model=UserIAM.UserIAMDB,
    status_code=status.HTTP_201_CREATED,
    tags=["IAM Users"],
    summary="Create method",
    description="Create an user based on it's infos and add a random uuid4 id",
)
async def add_user(user: UserIAM.UserIAMGeneral) -> UserIAM.UserIAMDB:
    user_dict = user.dict()
    user_dict["id"] = str(uuid4())
    db.users.append(UserIAM.UserIAMDB(**user_dict))
    return db.users[-1]


@app.delete(
    "/users/{user_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["IAM Users"],
    summary="Delete one method",
    description="Delete an user by it's ID",
)
async def delete_user(user_id: str) -> dict[str]:
    for user in db.users:
        if user.id == user_id:
            db.users.remove(user)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User found")


@app.post(
    "/terraform/{action}",
    status_code=status.HTTP_200_OK,
    tags=["Terraform"],
    summary="Run terraform apply | destroy",
    description="Return all instances in database",
)
async def post_destroy_apply(action: str):
    data = {"ingress": [], "instances": [], "users": []}
    [data["ingress"].append(i.dict()) for i in db.ingress]

    dic = {}
    i = 0
    for ec2 in db.instances:
        dic[f"instances {i}"] = ec2.dict()
        i += 1
    data["instances"] = dic

    dic = {}
    i = 0
    for name in db.users:
        dic[f"User {i}"] = name.dict()
        i += 1
    data["users"] = dic

    with open("variables.tfvars.json", "w") as openfile:
        json.dump(data, openfile)

    os.system(f"terraform {action} -auto-approve -var-file='variables.tfvars.json'")


@app.get(
    "/terraform/tfstate",
    status_code=status.HTTP_200_OK,
    tags=["Terraform"],
    summary="Get tfstate",
)
async def get_tfstate():
    output = {}
    with open("terraform.tfstate") as f:
        tfstate = json.load(f)

    for resource in tfstate["resources"]:
        if resource["type"] == "aws_iam_user":
            user = resource["instances"][0]["index_key"]
            output[f"aws_iam_user {user}"] = {
                "name": resource["instances"][0]["attributes"]["name"],
                "unique_id": resource["instances"][0]["attributes"]["unique_id"],
            }
        if resource["type"] == "aws_instance":
            ami = resource["instances"][0]["attributes"]["ami"]
            output[f"{ami}"] = {
                "availability_zone": resource["instances"][0]["attributes"][
                    "availability_zone"
                ],
                "vpc_security_group_ids": resource["instances"][0]["attributes"][
                    "vpc_security_group_ids"
                ],
                "instance_type": resource["instances"][0]["attributes"][
                    "instance_type"
                ],
                "subnet_id": resource["instances"][0]["attributes"]["subnet_id"],
            }
        if resource["type"] == "aws_security_group":
            output["aws_security_group"] = {
                "ingress_rules": resource["instances"][0]["attributes"]["ingress"],
            }
        if resource["type"] == "aws_subnet":
            output["aws_subnet"] = {
                "cidr_block": resource["instances"][0]["attributes"]["cidr_block"],
                "vpc_id": resource["instances"][0]["attributes"]["vpc_id"],
            }
        if resource["type"] == "aws_vpc":
            output["vpc_id"] = {
                "cidr_block": resource["instances"][0]["attributes"]["cidr_block"],
            }

    return output
