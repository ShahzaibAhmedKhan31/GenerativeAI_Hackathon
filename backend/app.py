from fastapi import FastAPI
from routes import recommend_router

# Initialize FastAPI app
app = FastAPI()

# Include the recommend router
app.include_router(recommend_router)