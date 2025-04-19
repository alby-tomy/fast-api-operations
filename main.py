from fastapi import FastAPI
from database import Base, engine
from controllers.user_controller import router as user_router
from controllers.product_info import router as product_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include the user routes
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(product_router, prefix="/product_info", tags=["Product Info"])