# C:\LLM\fastAPI\Summarisation>python -m uvicorn main:app --reload
# http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
import requests  
import os  

# Initialize FastAPI  
app = FastAPI()  

# Mistral API Configuration  
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "EqY4XkLDoEvrCuBg3DIsLJmTcd069wrT")  # Get from environment variable or replace  
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"  

# Pydantic model for input validation  
class SummarizationRequest(BaseModel):  
    text: str  # Changed from 'Story' to more generic 'text'  
    max_length: int = 150  # Optional parameter for summary length  

@app.post("/summarize")  
async def summarize_text(request: SummarizationRequest):  
    headers = {  
        "Authorization": f"Bearer {MISTRAL_API_KEY}",  
        "Content-Type": "application/json"  
    }  
    
    prompt = f"""  
    Create a concise summary of the following text in about {request.max_length} words.  
    Focus on the key points and maintain the original meaning:  
    
    {request.text}  
    """  
    
    payload = {  
        "model": "mistral-small",  # or mistral-medium for better quality  
        "messages": [  
            {"role": "user", "content": prompt}  
        ],  
        "temperature": 0.3,  # Lower for more factual summaries  
        "max_tokens": 300  
    }  

    try:  
        response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)  
        response.raise_for_status()  
        
        summary = response.json()["choices"][0]["message"]["content"]  
        
        return {  
            "original_length": len(request.text.split()),  
            "summary_length": len(summary.split()),  
            "summary": summary.strip()  
        }  
        
    except requests.exceptions.RequestException as e:  
        raise HTTPException(  
            status_code=500,  
            detail=f"Mistral API request failed: {str(e)}"  
        )  
    except Exception as e:  
        raise HTTPException(  
            status_code=500,  
            detail=f"Unexpected error: {str(e)}"  
        )  