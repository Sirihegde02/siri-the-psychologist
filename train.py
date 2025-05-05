import json
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Load intents.json
with open("intents.json") as f:
    data = json.load(f)

texts = []
labels = []
label_map = {}

for idx, intent in enumerate(data["intents"]):
    # Create unique list of intent tags
    tags = list({intent['tag'] for intent in data['intents']})
    label_map = {tag: idx for idx, tag in enumerate(tags)}
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            texts.append(pattern)
            labels.append(label_map[intent["tag"]])


# Convert to DataFrame
df = pd.DataFrame({"text": texts, "label": labels})
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Load tokenizer & prepare datasets
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    tokenized = tokenizer(
        batch["text"],
        padding="max_length",        # Ensures all inputs are the same length
        truncation=True,
        max_length=128,              # or 256 if needed
    )
    tokenized["label"] = batch["label"]
    return tokenized

train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=len(label_map)
)

# Training
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=4,
    per_device_train_batch_size=16,
    logging_steps=10,
    save_total_limit=1,
    save_strategy="epoch",            # <-- important!
    logging_dir="./results/logs",     # for TensorBoard
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

trainer.train()

# Save the model
model.save_pretrained("model")
tokenizer.save_pretrained("model")
