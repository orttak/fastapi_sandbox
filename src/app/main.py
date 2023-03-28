#source >>> https://testdriven.io/blog/fastapi-crud/#get-routes
#activate venv source activate fastapi
from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.routers import user,post,auth,vote
from app.database import  engine ,get_db
from app.config import settings

# heroku apps:destroy orttak-dd
# after set up alembci we don't need below command line arguments
#because alembic do it automatically
#models.Base.metadata.create_all(bind=engine)

app=FastAPI()
origin=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
# CORS middleware setting for different domains
from fastapi import Request, HTTPException

class AccessMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request,):
        allowed_domains = {
            "a.com": ["GET"],
            "b.com": ["GET", "POST", "PUT", "DELETE"]
        }
        domain = request.headers.get("host")
        if domain not in allowed_domains:
            raise HTTPException(status_code=403, detail="This domain is not allowed to make requests.")
        allowed_methods = allowed_domains[domain]
        if request.method not in allowed_methods:
            raise HTTPException(status_code=403, detail="This domain is not allowed to make this request.")
        response = await self.app(request)
        return response

from fastapi import FastAPI
from mymodule import AccessMiddleware

app = FastAPI()
app.add_middleware(AccessMiddleware)
"""

@app.get("/")
def root():
    return {"message":"Hello world"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




# """
# #first part of thiss app. Without DB
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating : Optional[int] = None

#my_post = [{"title":"My first post", "content":"This is my first post", "id":1},\
           #{"title":"My second post", "content":"This is my second post", "id":2}]

# def find_post(id):
#     for p in my_post:
#         if p["id"] == id:
#             return p

# @app.get("/posts")
# def get_posts():
# return model(input_data)
#     return {"data":my_post}

# @app.get("/posts/{post_id}")
# def get_post_by_id(post_id: int,response: Response):
#     target_post = find_post(post_id)
#     if not target_post:
#         raise HTTPException(status_code=404, \
#             detail="Post not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"detail":"Post not found"}
#     return {"data":target_post}

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# #we get json body as a dictionary
# def create_posts(post:Post):
#     post_dict=post.dict()
#     post_dict["id"]=len(my_post)+1
#     my_post.append(post_dict)
#     return {"data":post.dict()}
#     #return {"data":f"Succesfuly created post and your data is {new_post.content}"}

# @app.put("/posts/{post_id}")
# def update_post(post_id: int, post: Post):
#     target_post = find_post(post_id)
#     if not target_post:
#         raise HTTPException(status_code=404, \
#             detail="Post not found")
#     target_post.update(post.dict())
#     return {"data":target_post}

# @app.delete("/posts/{post_id}",status_code=204)
# def delete_post(post_id: int,):
#     target_post = find_post(post_id)
#     if not target_post: 
#         raise HTTPException(status_code=404, \
#             detail="Post not found")
#     my_post.remove(target_post)
#     #this is rule. we don't return anything
#     return Response(status_code=status.HTTP_204_NO_CONTENT,detail="Post deleted") 
   
# @app.post("/createPosts")
# #we get json body as a dictionary
# def create_posts(payload: dict =Body(...)):
#     print(payload)
#     return {"data":f"Succesfuly created post and your data is {payload['data']}"}