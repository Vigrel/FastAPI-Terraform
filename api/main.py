import json
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status

from api.core.models import db_ingress, db_instances
from api.core.schemas import IngressRules, Instance

app = FastAPI()
os.system("terraform init")


@app.get(
    "/instances/",
    response_model=list[Instance.InstanceDB],
    status_code=status.HTTP_200_OK,
    tags=["Intances"],
    summary="Get all method",
    description="Return all instances in database",
)
async def get_instances() -> list[Instance.InstanceDB]:
    return db_instances.instances


@app.post(
    "/instances/",
    response_model=Instance.InstanceDB,
    status_code=status.HTTP_201_CREATED,
    tags=["Intances"],
    summary="Create method",
    description="Create a instance based on it's infos and add a random uuid4 id",
)
async def add_instance(instance: Instance.InstanceGeneral) -> Instance.InstanceDB:
    instance_dict = instance.dict()
    instance_dict["id"] = str(uuid4())
    db_instances.instances.append(Instance.InstanceDB(**instance_dict))
    return db_instances.instances[-1]


@app.delete(
    "/instances/{instance_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Intances"],
    summary="Delete one method",
    description="Delete a instance by it's ID",
)
async def delete_instance(instance_id: str) -> dict[str]:
    for instance in db_instances.instances:
        if instance.id == instance_id:
            db_instances.instances.remove(instance)
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
    return db_ingress.ingress


@app.post(
    "/ingress/",
    response_model=IngressRules.IngressDB,
    status_code=status.HTTP_201_CREATED,
    tags=["IngressRules"],
    summary="Create method",
    description="Create a IngressRules based on it's infos and add a random uuid4 id",
)
async def add_ingress(ingress: IngressRules.IngressGeneral) -> IngressRules.IngressDB:
    ingress_dict = ingress.dict()
    ingress_dict["id"] = str(uuid4())
    db_ingress.ingress.append(IngressRules.IngressDB(**ingress_dict))
    return db_ingress.ingress[-1]


@app.delete(
    "/ingress/{rule_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["IngressRules"],
    summary="Delete one method",
    description="Delete a IngressRules by it's ID",
)
async def delete_ingress_rule(rule_id: str) -> dict[str]:
    for rule in db_ingress.ingress:
        if rule.id == rule_id:
            db_ingress.ingress.remove(rule)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")


@app.post(
    "/terraform/{action}",
    # response_model=list[Instance.InstanceDB],
    status_code=status.HTTP_200_OK,
    tags=["Terraform"],
    summary="Run terraform apply | destroy",
    description="Return all instances in database",
)
async def get_destroy_apply(action: str):
    data = {"ingress": []}
    [data["ingress"].append(i.dict()) for i in db_ingress.ingress]

    dic = {}
    i = 0
    for ec2 in db_instances.instances:
        dic[f"instances {i}"] = ec2.dict()
        i += 1

    data["instances"] = dic

    with open("variables.tfvars.json", "w") as openfile:
        json.dump(data, openfile)

    os.system(f"terraform {action} -auto-approve -var-file='variables.tfvars.json'")
