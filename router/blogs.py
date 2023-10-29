from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from schemas.blog_schema import BlogBase,UpdateArticle
from schemas.user_schema import UserBase, UserCreate #user_fullnames

from datetime import datetime
# from typing import List

import uuid
import csv

def generate_unique_id():
    return str(uuid.uuid4())

def get_date_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Get email address and password from users.csv file.
def get_user(email: str):
    with open("users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"] == email:
                return UserCreate(email=row["email"], password=row["password"])
    return None

# we hope to reutrn email, password,

# Function to verify that username and password are correct
def authenticate_user(credentials: UserCreate):
    # Check user credentials in the user data CSV file
    with open("users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for user in reader:
            if user["email"] == credentials.email and user["password"] == credentials.password:
                return credentials
    return None


blogs_router = APIRouter()

# Get the list of all blogs on the website.

@blogs_router.get("/get_blogs/")
async def get_blogs():
    blogs = []

    with open("blogs.csv") as file:
        reader = csv.DictReader(file)

        for row in reader:
            blogs.append({"id":row["id"],"author":row["author"],"title":row["title"],"content":row["content"],"date_created":row["date_created"]})   #,{"city":row["city"]}
     
        return(blogs)


#create a new blog



@blogs_router.post("/newblog")
async def add_blog(item: BlogBase, email: UserCreate = Depends(authenticate_user)):
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    item_id = generate_unique_id()
    created_date = get_date_time()

    with open("blogs.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([item_id,email.email,created_date, item.title, item.author, item.content])
    return {"id":item_id,"email": email,"created_date":created_date,**item.dict()}



def read_csv(file_path):
    with open(file_path, mode="r") as file:
        return list(csv.DictReader(file))
    
def write_to_csv(file_path, data):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


@blogs_router.put("/update_blog/{article_uuid}") #, response_model=BlogBase
async def update_blog(
updated_data: UpdateArticle,
article_uuid: str = Path(..., description="Article UUID"),
email: UserCreate = Depends(authenticate_user)
):
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")


    updated_blogs = read_csv("blogs.csv")
    found = False
    for row in updated_blogs:
            if row["email"] == email.email:
                if row["id"] == article_uuid:
                    # Update the title and content for the specific article
                    row["title"] = updated_data.updated_title
                    row["content"] = updated_data.updated_content
                    found = True

    if not found:
        raise HTTPException(status_code=404, detail="The id specified does not exist among your articles")

    write_to_csv("blogs.csv", updated_blogs)

    return updated_data

