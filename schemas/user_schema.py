from pydantic import BaseModel

import csv

class UserBase(BaseModel):
    # id: int
    firstname: str
    surname: str
    email: str
    age: int
    password: str




class UserCreate(BaseModel):
    email: str
    password: str


