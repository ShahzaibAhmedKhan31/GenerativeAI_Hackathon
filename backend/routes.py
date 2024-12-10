from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from helper_functions import recommendEvents, load_biking_events
import json

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

        # Call recommendation function
        recommended_events = recommendEvents(biking_events, user_calendar_events, user_information)

        return recommended_events

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="Biking events data file not found.")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Error decoding JSON from biking events data.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    

@recommend_router.post("/events")
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
