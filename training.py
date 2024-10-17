import os
import pandas as pd
import cleaning_tool as ct
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer
from datasets import Dataset
import evaluate
import numpy as np
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, EarlyStoppingCallback


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
    
def makeDataset(current, labels, tokenizer):
    inputs = tokenizer(current, padding=True, truncation=True, return_tensors='pt', max_length=128).to("cuda")
    
    return Dataset.from_dict({
    'input_ids': inputs['input_ids'],
    'attention_mask': inputs['attention_mask'],
    'labels': labels
})


#Setting GPU
os.environ["CUDA_VISIBLE_DEVICES"]="1"

# Load your dataset
df = pd.read_csv('training_set.csv')
df = df.dropna()
df = ct.filter_single_users(dataframe=df, min_pull=5)
print("data loaded")

# Encode the assignee names
label_encoder = LabelEncoder()
df['assignee_encoded'] = label_encoder.fit_transform(df['assignee'])

df['input_text'] = "<#TITLE-START#> " + df['title'] + " <#TITLE-END#> <#BODY-START#> " + df['body'] + " <#BODY-END#>"

trainingSet = df[df['number'] < 185000]['input_text'].tolist()
evaluationSet = df[ (185000 <= df['number']) & (df['number']< 210000)]['input_text'].tolist()
testSet = df[ 210000 <= df['number']]['input_text'].tolist()

labels = df['assignee_encoded'].tolist()

trainingLabels = df[df['number'] < 185000]['assignee_encoded'].tolist()
evaluationLabels = df[ (185000 <= df['number']) & (df['number']< 210000)]['assignee_encoded'].tolist()
testLabels = df[ 210000 <= df['number']]['assignee_encoded'].tolist()

model_name = 'distilbert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)

trainingSet = makeDataset(trainingSet, trainingLabels, tokenizer)
evaluationSet =  makeDataset(evaluationSet, evaluationLabels, tokenizer)
testSet =  makeDataset(testSet, testLabels, tokenizer)

# Load metric functions
accuracy_metric = evaluate.load('accuracy')
precision_metric = evaluate.load('precision')
recall_metric = evaluate.load('recall')
f1_metric = evaluate.load('f1')

# Load the model
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(label_encoder.classes_))

# Define training arguments with early stopping and final model saving
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='epoch',  # Evaluate at the end of each epoch
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    num_train_epochs=30,
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
    train_dataset=trainingSet,
    eval_dataset=evaluationSet,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],  # Early stopping with patience
)

# Train the model
trainer.train()

#Evaluate the model
trainer.evaluate(testSet)

print('FINISHED')

