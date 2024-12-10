from fastapi import HTTPException
from groq import Groq
import json
import os
from prompts import Openai_prompt, Groq_prompt

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def recommendEvents(biking_events, user_calendar_events, user_information):
    try:
        # Initialize the ChatOpenAI model
        chat_model = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))

        # Create an LLMChain with the prompt and model
        chain = LLMChain(llm=chat_model, prompt=PromptTemplate(
            input_variables=["Upcomming_Biking_Events", "Calendar_Availability", "User_Information"],
            template=Openai_prompt,
        ))

        # Run the chain with inputs
        result = chain.run({
            "Upcomming_Biking_Events": biking_events,
            "Calendar_Availability": user_calendar_events,
            "User_Information": user_information
        })

        # Serialize the result and match events
        serialize_output = SerializeOutput_Groq(result)
        events = matchedEvents(biking_events, serialize_output)

        return events

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in recommendEvents: {str(e)}")

def SerializeOutput_Groq(result):
    try:
        # Request the chat completion from Groq API
        chat_completion = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),  # Use the model that fits your requirements
            messages=[
                {"role": "system", "content": Groq_prompt},
                {"role": "user", "content": result}
            ],
        )

        cleaned_response = chat_completion.choices[0].message.content.strip()
        serialize_output = json.loads(cleaned_response)

        return serialize_output

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse Groq API response as JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in SerializeOutput_Groq: {str(e)}")

def matchedEvents(biking_events, serialize_output):
    try:
        matched_events = []

        for event in biking_events:
            event_date_str = event["event"]["date"]

            if event_date_str in serialize_output:
                matched_events.append(event)

        return matched_events

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing expected key in event data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in matchedEvents: {str(e)}")

def load_biking_events():
    try:
        events_file_path = os.getenv("EVENT_DATA_PATH")

        if not os.path.exists(events_file_path):
            raise FileNotFoundError(f"Event data file {events_file_path} not found.")

        with open(events_file_path, 'r') as file:
            biking_events = json.load(file)

        return biking_events

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="Event data file not found.")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Failed to decode JSON from event data file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading biking events: {str(e)}")
