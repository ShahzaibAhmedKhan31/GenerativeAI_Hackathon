from fastapi import FastAPI
from routes import recommend_router
from fastapi.staticfiles import StaticFiles
import uvicorn

# Initialize FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the recommend router
app.include_router(recommend_router)
