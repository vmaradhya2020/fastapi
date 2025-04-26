# C:\LLM\fastAPI\Summarisation>python -m uvicorn main_google:app --reload
# http://127.0.0.1:8000/docs

from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Set up the generative AI model
genai.configure(api_key="AIzaSyAOAjnggIYeBjjXL8M-ZyGmMQ-nBVVCDog")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize FastAPI
app = FastAPI()

# Pydantic model for input validation
class StoryRequest(BaseModel):
    Story: str

# POST endpoint for generating a story based on the title
@app.post("/Summarize")
async def generate_story(request: StoryRequest):
    # Get the title from the request
    Story = request.Story
    
    # Generate story using the provided title
    response = model.generate_content([f"Please summarize the following text:\n\n{Story}"])
    
    # Return the generated story as a response
    return {"Story": Story, "Summmary": response.text}

