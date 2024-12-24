from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer
import onnx

# example with distilbert model
model_checkpoint = "distilbert_trainer"
save_directory = "distibert_onnx/"

# Load a model from transformers and export it to ONNX
ort_model = ORTModelForSequenceClassification.from_pretrained(model_checkpoint, export=True)
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

# Save the onnx model and tokenizer
ort_model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

# Check the onnx model
onnx_model = onnx.load("distibert_onnx\\model.onnx")
onnx.checker.check_model(onnx_model)