import logging
import json
import uvicorn
from pydantic import BaseModel
from transformers import pipeline
from logging_config import setup_logging
from fastapi import FastAPI, HTTPException

config_path = 'config.json'
with open(config_path, 'r') as f:
    config_data = json.load(f)

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

# Health Check
@app.get("/health_status")
def health_status():
    return {"status": "healthy"}

# Start Uvicorn server if script is run directly
if __name__ == "__main__":
    setup_logging("logs")  # Set log directory
    uvicorn.run(app, host="0.0.0.0", port=8000)