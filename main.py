from fastapi import FastAPI

from router.users import user_router
from router.blogs import blogs_router
# from schemas.blog_schema import Blog

app = FastAPI()

#register the routers
@app.get("/")
async def home_page():
    return {
        "Title": "Welcome Bloggers!!.",
        "introduction": "Great to have you here, This is a place you can view ideas, create new ones, share what is on your mind and enjoy every bit of it. In order to share what is on your mind, you will have to create an account and log. Enjoy your stay"
    }

app.include_router(user_router, prefix="/users", tags=["Users"])           
app.include_router(blogs_router, prefix="/blogs", tags = ["Blogs"] )   

