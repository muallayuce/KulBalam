from schemas import PostBase, PostDisplay, PostImage, PostUpdate, UserBase
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_post, db_user, db_post_images
from auth.oauth2 import get_current_user
from datetime import datetime

router = APIRouter(
    tags=['userwall']
)


@router.post("/posts")
def create_post(content: str, user_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    # Fetch the username associated with the provided user_id
    username = db_user.get_username(db=db, user_id=user_id)
    if not username:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the post with the provided user_id and fetched username
    new_post = db_post.create_post(
        db=db,
        request=PostBase(content=content, user_id=user_id, username=username, timestamp=datetime.now())
    )
    return new_post

#Inert image
@router.post('/posts/{id}/images', response_model=PostImage)
def upload_post_image(id: int, image: UploadFile = File(...), db: Session = Depends (get_db)):
    return db_post_images.upload_post_image(db, id, image)

@router.get('/images/{id}')
def get_image(id: int, db: Session = Depends (get_db)):
    return db_post_images.get_post_image(db, id)

@router.get('/postimage/all')
def get_all_images(db: Session = Depends(get_db)):
    return db_post_images.get_all_post_images(db)

# This endpoint is used to retrieve posts # Get all posts from User 
@router.get("/posts/all")
def posts(db: Session = Depends(get_db)):
    posts = db_post.get_all(db)
    return posts

#get spesific post
@router.get('/posts/{id}') #, response_model=PostDisplay)
def get_post(id:int, db:Session = Depends(get_db)): #secure end-point #token: str = Depends(oauth2_scheme)
    return {
        'data': db_post.get_post(db,id)
    }

#Update Post
@router.put('/posts/{id}', response_model=PostDisplay)
def update_post(id: int, request: PostUpdate, db: Session = Depends(get_db), current_user:UserBase = Depends(get_current_user)):
    # Check if the post exists
    post = db_post.get_post(db, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    # Update the post content and image_url
    post = db_post.update_post(db, id, request)
    
    return post


#Delete Post
@router.delete('/posts/{id}')
def delete_post(id:int, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_post.delete_post(db, id)





