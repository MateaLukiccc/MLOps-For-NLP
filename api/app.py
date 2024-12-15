import logging
import json
import uvicorn
from pydantic import BaseModel
from transformers import pipeline
from logging_config import setup_logging
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Pre-trained model from Hugging Face
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased")

# Define Pydantic model for input
class TextInput(BaseModel):
    text: str

# Predict function
@app.post("/predict")
async def predict(input_data: TextInput):
    try:
        # Get prediction
        prediction = classifier(input_data.text)
        return {"prediction": prediction}
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/health")
def health_check():
    return {"status": "OK"}

if __name__ == "__main__":
    setup_logging("logging") 
    uvicorn.run(app, host="0.0.0.0", port=8000)