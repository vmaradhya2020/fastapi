# C:\LLM\fastAPI\text-generation>python -m uvicorn main_google:app --reload
# http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException #FastAPI is a web framework for building APIs, HTTPException is a class that defines the structure of the data that is sent to the API
from pydantic import BaseModel #BaseModel is a class that defines the structure of the data that is sent to the API
import google.generativeai as genai #google.generativeai is a module that provides a client for the Google Generative AI API

# Set up the generative AI model
genai.configure(api_key="XXXXXXXXXXXXXXXXXXXx")  


# Set up the model configuration
generation_config = {
    "temperature": 0.2, #Temperature is a parameter that controls the randomness of the model's output.
    "top_p" : 0.8, #Top_p is a parameter that controls the diversity of the model's output.
    "top_k" : 64, #Top_k is a parameter that controls the number of tokens that the model can choose from.
    "max_output_tokens" : 8192, #Max_output_tokens is a parameter that controls the maximum number of tokens that the model can output.
    }

model = genai.GenerativeModel(
    model_name = "gemini-1.5-flash", 
    generation_config=generation_config,
)

# Funcion to translate text using the Gemini model.
def translate_text(text: str, source_language: str, target_language: str) -> str:
    # prompt = f"Translate the following text from {source_language} to {target_language}: {text}"]
    prompt = f"Translate the following text from and return only the translated text: {source_language} to {target_language}: {text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating translation: {str(e)}")

# Initialize FastAPI
app = FastAPI()

# Request model for input validation.
class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

# POST endpoint for generating a story based on the title
@app.post("/translate/")
async def translate(request: TranslationRequest):
    try:
        translated_text = translate_text(request.text, request.source_language, request.target_language)
        return {"original_text": request.text, "translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error translating text: {str(e)}")

