# C:\LLM\fastAPI\text-generation>python -m uvicorn main:app --reload
# http://127.0.0.1:8000/docs

from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Initialize FastAPI
app = FastAPI()

# Set up the generative AI model
genai.configure(api_key="AIzaSyAOAjnggIYeBjjXL8M-ZyGmMQ-nBVVCDog")  
model = genai.GenerativeModel("gemini-1.5-flash")

# Pydantic model for input validation
class StoryRequest(BaseModel):
    title: str

# POST endpoint for generating a story based on the title
@app.post("/story")
async def generate_story(request: StoryRequest):
    # Get the title from the request
    title = request.title
    
    # Generate story using the provided title
    response = model.generate_content(f"Write a very short story about a {title}")
    
    # Return the generated story as a response
    return {"title": title, "story": response.text}

