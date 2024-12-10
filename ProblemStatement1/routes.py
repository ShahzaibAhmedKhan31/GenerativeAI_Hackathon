from fastapi import Request, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from helper_functions import recommendEvents, load_biking_events
import json
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx
import os

from dotenv import load_dotenv

# load environment file
load_dotenv()


# Define the router
recommend_router = APIRouter()

# Define input model
class RecommendationRequest(BaseModel):
    user_calendar_events: list
    user_information: dict

@recommend_router.post("/recommend")
async def recommend_events(request: RecommendationRequest):
    try:
        # Load biking events
        biking_events = load_biking_events()

        # Extract user data from the request
        user_calendar_events = request.user_calendar_events
        user_information = request.user_information
        # print(user_calendar_events)
        # print(user_information)
        # Call recommendation function
        recommended_events = recommendEvents(biking_events, user_calendar_events, user_information)

        return recommended_events

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="Biking events data file not found.")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Error decoding JSON from biking events data.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


templates = Jinja2Templates(directory="templates")

# Google OAuth credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

@recommend_router.get("/home")
async def frontend(request: Request, access_token: str = None, id_token: str = None):
    # Pass the token to the frontend template
    return templates.TemplateResponse("home.html", {"request": request, "access_token": access_token, "id_token": id_token})

@recommend_router.get("/index")
async def index(request: Request):
    # Pass the token to the frontend template
    return templates.TemplateResponse("index.html", {"request": request})

@recommend_router.get("/navbar")
async def navbar(request: Request):
    # Pass the token to the frontend template
    return templates.TemplateResponse("navbar.html", {"request": request})

@recommend_router.get("/all-upcoming-events")
async def allupcomming(request: Request):
    # Pass the token to the frontend template
    return templates.TemplateResponse("all-upcoming-events.html", {"request": request})

@recommend_router.get("/view-profile")
async def viewprofile(request: Request):
    # Pass the token to the frontend template
    return templates.TemplateResponse("view-profile.html", {"request": request})

@recommend_router.get("/")
async def home():
    # Redirect to Google OAuth2 for authorization
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20email%20https://www.googleapis.com/auth/calendar"
    return RedirectResponse(auth_url)

@recommend_router.get("/auth")
async def auth(request: Request, code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Error: No authorization code received.")

    # Exchange the authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        id_token = token_data.get('id_token')
        print(id_token)
        # Redirect to the frontend home page with the access token as a query parameter
        return RedirectResponse(f'http://localhost:8000/home?access_token={access_token}&id_token={id_token}')
    else:
        raise HTTPException(status_code=400, detail="Failed to exchange authorization code for access token")


@recommend_router.get("/events")
async def get_upcoming_events():
    try:
        # Load biking events
        biking_events = load_biking_events()

        return biking_events

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="Biking events data file not found.")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Error decoding JSON from biking events data.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")