# C:\LLM\fastAPI\Translation>python -m uvicorn main:app --reload
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

# Translation configuration  
DEFAULT_TEMPERATURE = 0.3  # Lower for more accurate translations  

class TranslationRequest(BaseModel):  
    text: str  
    source_language: str  
    target_language: str  
    formality: str = "neutral"  # Optional: formal/informal/neutral  

def translate_text(text: str, source_lang: str, target_lang: str, formality: str = "neutral") -> str:  
    headers = {  
        "Authorization": f"Bearer {MISTRAL_API_KEY}",  
        "Content-Type": "application/json"  
    }  
    
    prompt = f"""  
    Translate the following text from {source_lang} to {target_lang}.  
    Maintain {formality} formality.  
    Return ONLY the translated text without any additional commentary or explanations.  
    
    Text to translate:  
    "{text}"  
    """  
    
    payload = {  
        "model": "mistral-small",  # or "mistral-medium" for better quality  
        "messages": [{"role": "user", "content": prompt}],  
        "temperature": DEFAULT_TEMPERATURE,  
        "max_tokens": len(text) * 3  # Allow enough tokens for translation  
    }  

    try:  
        response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)  
        response.raise_for_status()  
        return response.json()["choices"][0]["message"]["content"].strip()  
    except requests.exceptions.RequestException as e:  
        raise HTTPException(  
            status_code=502,  
            detail=f"Translation service unavailable: {str(e)}"  
        )  

@app.post("/translate/")  
async def translate(request: TranslationRequest):  
    try:  
        translated_text = translate_text(  
            request.text,  
            request.source_language,  
            request.target_language,  
            request.formality  
        )  
        return {  
            "original_text": request.text,  
            "translated_text": translated_text,  
            "language_pair": f"{request.source_language}→{request.target_language}"  
        }  
    except HTTPException:  
        raise  
    except Exception as e:  
        raise HTTPException(  
            status_code=500,  
            detail=f"Translation failed: {str(e)}"  
        )  