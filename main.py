from fastapi import FastAPI
from app import models
from app.database import engine

# Explicitly import the routers directly from their specific files
from app.routers.products import router as products_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router

# Auto-create database tables in MySQL
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory System Pro")

# Registering Routers explicitly
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Inventory Management System API"}