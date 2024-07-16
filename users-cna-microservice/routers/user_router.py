from typing import List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from db.dals.user_dal import UserDAL
from db.models.user import User
from dependencies import get_user_dal

router = APIRouter()

# Define Pydantic models for the User
class UserBase(BaseModel):
    id: int
    name: str
    email: str
    mobile: str

    class Config:
        orm_mode = True

@router.post("/users", response_model=UserBase)
async def create_user(name: str, email: str, mobile: str, user_dal: UserDAL = Depends(get_user_dal)) -> UserBase:
    print("name: " + name)
    user = await user_dal.create_user(name, email, mobile)
    return UserBase.from_orm(user)

@router.put("/users/{user_id}", response_model=UserBase)
async def update_user(user_id: int, name: Optional[str] = None, email: Optional[str] = None, mobile: Optional[str] = None,
                      user_dal: UserDAL = Depends(get_user_dal)) -> UserBase:
    user = await user_dal.update_user(user_id, name, email, mobile)
    return UserBase.from_orm(user)

@router.get("/users/{user_id}", response_model=UserBase)
async def get_user(user_id: int, user_dal: UserDAL = Depends(get_user_dal)) -> UserBase:
    user = await user_dal.get_user(user_id)
    return UserBase.from_orm(user)

@router.get("/users", response_model=List[UserBase])
async def get_all_users(user_dal: UserDAL = Depends(get_user_dal)) -> List[UserBase]:
    users = await user_dal.get_all_users()
    return [UserBase.from_orm(user) for user in users]
