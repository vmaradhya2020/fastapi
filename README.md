# fastapi =>  GitHub repository that covers all three FastAPI services (Summarization, Text Generation, and Translation) using Mistral and google AI:

# FastAPI LLM Microservices  

A collection of AI-powered microservices using FastAPI and Mistral AI:  
1. **Text Summarization**  
2. **Story Generation**   
3. **Text Translation**  

# For Summarization Service  
uvicorn summarization_app:app --reload --port 8000
python -m uvicorn main:app --reload (Invoke from terminal fron VS editor)

# For Story Generation Service   
uvicorn story_generation_app:app --reload --port 8001  
python -m uvicorn main:app --reload (Invoke from terminal fron VS editor)

# For Translation Service  
uvicorn translation_app:app --reload --port 8002  
python -m uvicorn main:app --reload (Invoke from terminal fron VS editor)
# 🌐 API Documentation
Access interactive docs at:
Summarization: http://localhost:8000/docs
Story Generation: http://localhost:8001/docs
Translation: http://localhost:8002/docs
