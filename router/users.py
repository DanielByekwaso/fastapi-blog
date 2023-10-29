from fastapi import APIRouter, HTTPException, Depends
from schemas.user_schema import UserBase, UserCreate


import uuid


import csv

user_router = APIRouter()


def is_email_unique(email):
    with open("users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"] == email:
                return False
    return True




@user_router.post("/register/", response_model=UserBase)
async def create_user(user: UserBase):
    if not is_email_unique(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    with open("users.csv", mode="a", newline="") as file:
        fieldnames = [user.firstname, user.surname, user.email, user.age, user.password]
        writer = csv.writer(file)
        writer.writerow(fieldnames)

    return user

