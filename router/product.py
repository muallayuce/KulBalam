from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from schemas import ProductBase, ProductDisplay, ProductImage, Review, ReviewDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_product, db_images, db_review, db_product

router = APIRouter(
    prefix='/products',
    tags=['products']
)

#Insert product
@router.post('/', response_model=ProductDisplay)
def insert_product(request: ProductBase, db: Session = Depends(get_db)):
    return db_product.insert_product(db, request)

#Get a product by id
@router.get('/{id}', response_model=ProductDisplay)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return db_product.get_product_by_id(db, id)

#Get products
@router.get('/', response_model=List[ProductDisplay])
def get_product( db: Session = Depends (get_db), product_name: str=''): #str='' for query parameter
    return db_product.get_all_products(db, product_name)

#Update a product
@router.put('/{id}',  response_model=ProductDisplay)
def update_product(id: int, product_name: str, description: str, price: float, quantity: int, db: Session = Depends (get_db)):
    return db_product.update_product(db, id, product_name,description, price, quantity )

#Delete a product
@router.delete('/{id}')
def delete_product(id:int, db:Session = Depends(get_db)):
    return db_product.delete_product(db, id)

#Inert image
@router.post('/{id}/images', response_model=ProductImage)
def upload_product_image(id: int, image: UploadFile = File(...), db: Session = Depends (get_db)):
    return db_images.upload_product_image(db, id, image)

#Create product review
@router.post('/{id}/reviews', response_model=ReviewDisplay)
def create_review(id: int, creator_id: int, request: Review, db: Session = Depends(get_db)):
    return db_review.create_review(db, id, creator_id, request)

#Get all reviews of a product
@router.get("/{id}/reviews")
def get_reviews(id: int, db: Session = Depends(get_db)):
    reviews = db_review.get_all_product_reviews(db, id)
    return {'reviews': reviews}