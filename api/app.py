import logging
import os
import json
import uvicorn
import onnxruntime as ort
import numpy as np
from pydantic import BaseModel
from logging_config import setup_logging
from fastapi import FastAPI, HTTPException
from transformers import ElectraTokenizer

app = FastAPI()

MODEL_DIR = "electra_onnx"
MODEL_PATH = os.path.join(MODEL_DIR, "model.onnx")
TOKENIZER_PATH = MODEL_DIR 

tokenizer = ElectraTokenizer.from_pretrained(TOKENIZER_PATH, local_files_only=True) 
onnx_session = ort.InferenceSession(MODEL_PATH)

class TextInput(BaseModel):
    text: str

def predict_onnx(text: str):
    try:
        tokens = tokenizer(
            text,
            return_tensors="np",
            padding=True,
            truncation=True,
            max_length=512,
        )

        ort_inputs = {
            onnx_session.get_inputs()[0].name: tokens["input_ids"],
            onnx_session.get_inputs()[1].name: tokens["attention_mask"],
            onnx_session.get_inputs()[2].name: tokens["token_type_ids"]
        }
        ort_outs = onnx_session.run(None, ort_inputs)

        logits = ort_outs[0]
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=1, keepdims=True)
        labels = ["World", "Sports", "Business", "Sci/Tech"]

        predicted_label = labels[np.argmax(probabilities)]
        confidence = np.max(probabilities)

        return {"label": predicted_label, "confidence": float(confidence)}
    except Exception as e:
        logging.error(f"Error in ONNX prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during prediction")

# Predict function
@app.post("/predict")
async def predict(input_data: TextInput):
    return predict_onnx(input_data.text)


@app.get("/health")
def health_check():
    return {"status": "OK"}

if __name__ == "__main__":
    setup_logging("logging") 
    uvicorn.run(app, host="0.0.0.0", port=8000)