import secrets
import smtplib
import string
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from random import random

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List

from .models import User, Product, License, ResetPasswordRequest, ResetPassword
from .db import db

from passlib.hash import bcrypt
from cryptography.fernet import Fernet

router = APIRouter()

#PASSWORD RESET

# Route for requesting a password reset
@router.post("/forgot-password")
async def forgot_password(request: ResetPasswordRequest):
    user = db.users.find_one({"email": request.email})
    if user:
        # Generate a unique token
        token = secrets.token_urlsafe(32)
        # Store the token with an expiration time (e.g., 24 hours)
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        db.password_reset_tokens.insert_one({
            "token": token,
            "email": request.email,
            "expiration_time": expiration_time
        })
        # Send email with password reset link containing the token
        send_password_reset_email(request.email, token)
        return {"message": "Password reset link sent to your email"}
    raise HTTPException(status_code=404, detail="User not found")

def send_password_reset_email(email: str, token: str):
    msg = MIMEText(f"Click the link to reset your password: http://172.20.10.2:9999/reset-password?token={token}")
    msg["Subject"] = "Password Reset Request"
    msg["From"] = "Your Name <Nihaldm.214@gmail.com>"
    msg["To"] = email

    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login("Nihaldm.214@gmail.com", "ejyg idhd udeq jlcx")
        smtp_server.send_message(msg)
        smtp_server.quit()
    except Exception as e:
        print("Error sending email:", e)

# Route for resetting the password with a valid token
@router.post("/reset-password")
async def reset_password(reset_data: ResetPassword):
    # Check if the token exists and is not expired
    token_data = db.password_reset_tokens.find_one({"token": reset_data.token})
    if token_data and token_data["expiration_time"] > datetime.utcnow():
        # Hash the new password
        hashed_password = bcrypt.hash(reset_data.new_password)
        # Update the user's password in the database
        db.users.update_one({"email": token_data["email"]}, {"$set": {"password": hashed_password}})
        # Invalidate or delete the used token
        db.password_reset_tokens.delete_one({"token": reset_data.token})
        return {"message": "Password reset successful"}
    raise HTTPException(status_code=400, detail="Invalid or expired token")







#USERS ENDPOINT


# Endpoint to get the _id for a username
@router.get("/get-user-id/")
async def get_user_id(username: str):
    user = db.users.find_one({"username": username})
    if user:
        return {"username": user["username"], "_id": str(user["_id"])}
    raise HTTPException(status_code=404, detail="User not found")


# Add new route to create a user with hashed password
@router.post("/users/", response_model=User)
async def create_user(user: User):
    # Hash the password before storing it
    hashed_password = bcrypt.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    inserted_user = db.users.insert_one(user_data)
    return {**user.dict(), "_id": str(inserted_user.inserted_id)}



# Update existing route to handle password updates
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    try:
        user_obj_id = ObjectId(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user_data = user.dict(exclude_unset=True)
    # Hash the password if it's included in the update
    if "password" in user_data:
        user_data["password"] = bcrypt.hash(user_data["password"])

    updated_user = db.users.find_one_and_update(
        {"_id": user_obj_id}, {"$set": user_data}, return_document=True
    )
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")




# Get all users with user IDs included
@router.get("/users/", response_model=List[dict])
async def get_all_users():
    # Retrieve all users from the database with their IDs
    users = list(db.users.find())
    # Add the user IDs to the user data before returning
    users_with_ids = [{**user, "_id": str(user["_id"])} for user in users]
    return users_with_ids

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    try:
        user_obj_id = ObjectId(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = db.users.find_one({"_id": user_obj_id})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")



@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    try:
        user_obj_id = ObjectId(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    deleted_user = db.users.find_one_and_delete({"_id": user_obj_id})
    if deleted_user:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")








@router.post("/products/", response_model=Product)
async def create_product(product: Product):
    product_data = product.dict()
    inserted_product = db.products.insert_one(product_data)
    return {**product.dict(), "_id": str(inserted_product.inserted_id)}

@router.get("/products/", response_model=List[dict])
async def get_all_products():
    products = list(db.products.find())
    products_with_ids = [{**product, "_id": str(product["_id"])} for product in products]
    return products_with_ids

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    try:
        product_obj_id = ObjectId(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = db.products.find_one({"_id": product_obj_id})
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: Product):
    try:
        product_obj_id = ObjectId(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product_data = product.dict(exclude_unset=True)
    updated_product = db.products.find_one_and_update(
        {"_id": product_obj_id}, {"$set": product_data}, return_document=True
    )
    if updated_product:
        return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    try:
        product_obj_id = ObjectId(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")

    deleted_product = db.products.find_one_and_delete({"_id": product_obj_id})
    if deleted_product:
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")







@router.post("/licenses/", response_model=License)
async def create_license(user_id: str, product_id: str):
    # Check if the user and product exist
    user = db.users.find_one({"_id": ObjectId(user_id)})
    product = db.products.find_one({"_id": ObjectId(product_id)})
    if not user or not product:
        raise HTTPException(status_code=404, detail="User or Product not found")

    # Generate a unique license key
    license_key = secrets.token_hex(16)  # Generate a 32-character hexadecimal token

    # Calculate expiry date (current date + 2 years)
    current_date = datetime.utcnow()
    expiry_date = current_date + timedelta(days=730)  # 2 years = 730 days

    # Create the license object
    license_data = {
        "license_key": license_key,
        "product_id": product_id,
        "user_id": user_id,
        "issued_date": current_date.isoformat(),
        "expiry_date": expiry_date.isoformat(),
        "status": "active"
    }

    # Insert the license into the database
    inserted_license = db.licenses.insert_one(license_data)

    # Return the created license with its generated _id
    return {**license_data, "_id": str(inserted_license.inserted_id)}


@router.get("/licenses/", response_model=List[dict])
async def get_all_licenses():
    licenses = list(db.licenses.find())
    licenses_with_ids = [{**license, "_id": str(license["_id"])} for license in licenses]
    return licenses_with_ids

@router.get("/licenses/{license_id}", response_model=License)
async def get_license(license_id: str):
    try:
        license_obj_id = ObjectId(license_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid license ID")

    license = db.licenses.find_one({"_id": license_obj_id})
    if license:
        return license
    raise HTTPException(status_code=404, detail="License not found")

@router.put("/licenses/{license_id}", response_model=License)
async def update_license(license_id: str, license: License):
    try:
        license_obj_id = ObjectId(license_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid license ID")

    license_data = license.dict(exclude_unset=True)
    updated_license = db.licenses.find_one_and_update(
        {"_id": license_obj_id}, {"$set": license_data}, return_document=True
    )
    if updated_license:
        return updated_license
    raise HTTPException(status_code=404, detail="License not found")

@router.delete("/licenses/{license_id}", response_model=dict)
async def delete_license(license_id: str):
    try:
        license_obj_id = ObjectId(license_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid license ID")

    deleted_license = db.licenses.find_one_and_delete({"_id": license_obj_id})
    if deleted_license:
        return {"message": "License deleted successfully"}
    raise HTTPException(status_code=404, detail="License not found")

