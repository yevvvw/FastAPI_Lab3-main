from fastapi import APIRouter, status, Response, Path, Depends
from typing import Union, List
from apps import models, scheme, crud
from utils.defaultResponse import DefaultResponse
from apps.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api",
    tags=["user"]
)

responses = {
    status.HTTP_404_NOT_FOUND: {"model": DefaultResponse, "description": "Item not found"}
}


@router.get("/users/", response_model=Union[List[scheme.User], None], status_code=status.HTTP_200_OK)
def read_users(db: Session = Depends(get_db)):
    all_users = crud.get_all(models.User, db)
    return all_users


@router.get("/users/{id}", response_model=Union[scheme.User, DefaultResponse],
            responses={**responses, status.HTTP_200_OK: {"model": scheme.User}})
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user: models.User = crud.get_by_id(models.User, id, db)
    if user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")

    return user


@router.post("/users", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
def create_user(user: scheme.CreateUser, db: Session = Depends(get_db)):
    crud.create(models.User, user, db)
    return DefaultResponse(success=True, message="User successfully created")


@router.put("/users", response_model=Union[scheme.UpdateUser, DefaultResponse],
            responses={**responses, status.HTTP_200_OK: {"model": scheme.User}})
def update_user(user: scheme.UpdateUser, response: Response, db: Session = Depends(get_db)):
    updated_user: scheme.User = crud.update(models.User, user, db)
    if updated_user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")

    return updated_user


@router.patch("/users", response_model=Union[scheme.PatchUser, DefaultResponse],
              responses={**responses, status.HTTP_200_OK: {"model": scheme.User}})
def patch_user(user: scheme.PatchUser, response: Response, db: Session = Depends(get_db)):
    updated_user: scheme.User = crud.update(models.User, user, db)
    if updated_user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")

    return updated_user


@router.delete("/users/{id}", response_model=DefaultResponse,
               responses={**responses, status.HTTP_200_OK: {"model": DefaultResponse}})
def remove_user(id: int, response: Response, db: Session = Depends(get_db)):
    user: models.User = crud.get_by_id(models.User, id, db)
    if user == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return DefaultResponse(success=False, message="User not found")

    crud.delete(models.User, id, db)

    return DefaultResponse(success=True, message="User successfully removed")