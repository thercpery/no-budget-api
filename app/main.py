from fastapi import FastAPI
from core.middlewares import database
from core.routers import Products
from core.routers import Users

app = FastAPI()


@app.on_event("startup")
async def startup_db():
    global db
    try:
        db = database.db
        print("Connected to MongoDB database ", db)
    except Exception as e:
        print(f"Something happened, {e}")


@app.on_event("shutdown")
async def shutdown_db():
    print("Shutting down server")
    db.close()


@app.get("/")
async def index():
    return {
        "message":
            "No-Budget Shop API: We'll drain your wallet more by selling second-hand products that you don't need."
    }

app.include_router(Products.router, tags=["products"], prefix="/api/products")
app.include_router(Users.router, tags=["users"], prefix="/api/users")
