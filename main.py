from pathlib import Path
from typing import Any
from flask import Flask
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import json
import torch

# global objects initialised later, does python even need to declare them like this???
model: Any
tokenizer: Any
labels: Any

app: Any

if __name__ == '__main__':
    model_path: Path = Path("./results/checkpoint-18759")
    model_name: str = "distilbert-base-uncased"
    model = AutoModelForSequenceClassification.from_pretrained(model_path.as_posix())
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Check if CUDA is available
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    model.to(device)

    label_path: Path = Path("./labels_json.json")
    with open(label_path) as f:
        labels = json.load(f)

    port = 3000
    host = "0.0.0.0"
    app = Flask(__name__, template_folder="../templates")
    app.run(port=port, host=host)

