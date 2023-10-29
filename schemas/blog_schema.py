from pydantic import BaseModel


import csv


class BlogBase(BaseModel):
    # id: int
    # username: str
    title: str
    author: str
    content: str

class UpdateArticle(BaseModel):
    #email: str
    #article_uuid: str
    updated_title: str
    updated_content: str

    
