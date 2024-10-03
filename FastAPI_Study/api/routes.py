from fastapi import APIRouter, Depends, HTTPException
from FastAPI_Study.db.repository import UserRepository
from FastAPI_Study.schemas.user import UserInDB, UserInfo

api_router = APIRouter()


# получаю экземпляр репозитория
def get_user_repository():
    return UserRepository()


# эндпоинт для регистрации создания пользователя
@api_router.post("/users/", response_model=dict)
async def create_user(user: UserInfo, repo: UserRepository = Depends(get_user_repository)):
    user_id = await repo.create_user(user)
    if user_id:
        return {
            "status": "success",
            "message": "User created successfully",
            "data": UserInDB(user_id=user_id, **user.dict())
        }
    raise HTTPException(status_code=400, detail="User could not be created")


# эндпоинт для получения пользователя по id
@api_router.get("/users/{user_id}", response_model=dict)
async def get_user_by_id(user_id: int, repo: UserRepository = Depends(get_user_repository)):
    user = await repo.get_user_by_id(user_id)
    if user:
        return {
            "status": "success",
            "message": f"User with id {user_id} found",
            "data": user
        }
    raise HTTPException(status_code=404, detail="User not found")


# эндпоинт для вывода всех пользователей
@api_router.get("/users/", response_model=dict)
async def list_all_users(repo: UserRepository = Depends(get_user_repository)):
    users = await repo.list_all_users()
    if users:
        return {
            "status": "success",
            "message": "List of all users",
            "data": users
        }
    raise HTTPException(status_code=404, detail="No users found")


# эндпоинт для обновления данных пользователя по id
@api_router.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, user: UserInfo, repo: UserRepository = Depends(get_user_repository)):
    existing_user = await repo.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    await repo.update_user(user_id, user)
    return {
        "status": "success",
        "message": f"User with id {user_id} updated successfully",
        "data": UserInDB(user_id=user_id, **user.dict())
    }


# эндпоинт для удаления пользователя
@api_router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, repo: UserRepository = Depends(get_user_repository)):
    existing_user = await repo.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    await repo.delete_user(user_id)
    return {
        "status": "success",
        "message": f"User with id {user_id} deleted successfully"
    }
