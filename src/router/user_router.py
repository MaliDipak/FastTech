from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

from src.schema.user_add_schema import AddUser
from src.schema.user_update_schema import UpdateUser
from src.service.user_service import UserService


# User Router
router = APIRouter(prefix="/user", tags=["User"])


#
# Public Routes
#

@router.post("/")
def add_user(user: AddUser):
    new_user = UserService.add_user(user)
    return JSONResponse(
        status_code=201,
        content={"status": "Success",
                 "message": "User Added", "user": new_user}
    )


#
# Protected Routes
#

@router.get("/")
def get_all_users():
    users = UserService.get_all_users()
    return JSONResponse(
        status_code=200,
        content={"status": "Success", "size": len(users), "users": users}
    )


@router.get("/{user_id}")
def get_user_by_id(user_id: int = Path(..., example=1, description="Get user by ID")):
    user = UserService.get_user_by_id(user_id)
    return JSONResponse(
        status_code=200,
        content={"status": "Success", "user": user}
    )


@router.put("/{user_id}")
def update_user(user: UpdateUser, user_id: int = Path(..., example=1, description="Update user by ID")):
    updated_user = UserService.update_user(update_user=user, user_id=user_id)
    return JSONResponse(
        status_code=200,
        content={"status": "Success",
                 "message": "User Updated Successfully", "user": updated_user}
    )
