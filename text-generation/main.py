# C:\LLM\fastAPI\text-generation>python -m uvicorn main_google:app --reload
# http://127.0.0.1:8000/docs

from fastapi import FastAPI  
from pydantic import BaseModel  
import requests  # For making API calls to Mistral  

app = FastAPI()  

# Mistral API configuration  
MISTRAL_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXX"  # Replace with your actual key  
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"  

class StoryRequest(BaseModel):  
    title: str  

@app.post("/story")  
async def generate_story(request: StoryRequest):  
    headers = {  
        "Authorization": f"Bearer {MISTRAL_API_KEY}",  
        "Content-Type": "application/json"  
    }  
    
    payload = {  
        "model": "mistral-tiny",  # or "mistral-small", "mistral-medium"  
        "messages": [  
            {"role": "user", "content": f"Write a very short story about a {request.title}"}  
        ],  
        "temperature": 0.7  
    }  

    try:  
        response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)  
        response.raise_for_status()  
        story = response.json()["choices"][0]["message"]["content"]  
        
        return {  
            "title": request.title,  
            "story": story.strip()  
        }  
        
    except Exception as e:  
        return {  
            "error": f"Failed to generate story: {str(e)}",  
            "api_response": response.json() if 'response' in locals() else None  
        }  
