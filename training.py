import os
import pandas as pd
import cleaning_tool as ct
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer
from datasets import Dataset
import evaluate
import numpy as np
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, EarlyStoppingCallback


#Setting GPU
os.environ["CUDA_VISIBLE_DEVICES"]="1"

# Load your dataset
df = pd.read_csv('cleaned_output2.csv')
df = df.dropna()
df = ct.filter_single_users(dataframe=df, min_pull=5)


# Encode the assignee names
label_encoder = LabelEncoder()
df['assignee_encoded'] = label_encoder.fit_transform(df['assignee'])
df['input_text'] = "<#TITLE-START#> " + df['title'] + " <#TITLE-END#> <#BODY-START#> " + df['body'] + " <#BODY-END#>"

# Split into input features (titles) and labels (encoded assignees)
titles = df['input_text'].tolist()
labels = df['assignee_encoded'].tolist()

model_name = 'distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenize the input titles
inputs = tokenizer(titles, padding=True, truncation=True, return_tensors='pt', max_length=128).to("cuda")

# Create a Hugging Face dataset
dataset = Dataset.from_dict({
    'input_ids': inputs['input_ids'],
    'attention_mask': inputs['attention_mask'],
    'labels': labels
})

# Split the dataset into training and validation sets
train_test = dataset.train_test_split(test_size=0.2)
train_dataset = train_test['train']
test_dataset = train_test['test']

# Load metric functions
accuracy_metric = evaluate.load('accuracy')
precision_metric = evaluate.load('precision')
recall_metric = evaluate.load('recall')
f1_metric = evaluate.load('f1')

# Define compute metrics function
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    
    accuracy = accuracy_metric.compute(predictions=predictions, references=labels)
    precision = precision_metric.compute(predictions=predictions, references=labels, average='weighted', zero_division=0)
    recall = recall_metric.compute(predictions=predictions, references=labels, average='weighted')
    f1 = f1_metric.compute(predictions=predictions, references=labels, average='weighted')
    
    return {
        'accuracy': accuracy['accuracy'],
        'precision': precision['precision'],
        'recall': recall['recall'],
        'f1': f1['f1'],
    }

# Load the model
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(label_encoder.classes_))

# Define training arguments with early stopping and final model saving
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='epoch',  # Evaluate at the end of each epoch
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    num_train_epochs=3,
    weight_decay=0.01,
    save_strategy='epoch',  # Save at the end of each epoch
    save_total_limit=1,  # Keep only the most recent model
    load_best_model_at_end=True,  # Automatically load the best model at the end
    metric_for_best_model='eval_loss',  # Use validation loss to select the best model
    greater_is_better=False,  # Lower loss is better
)

# Create the Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],  # Early stopping with patience
)

# Train the model
trainer.train()

