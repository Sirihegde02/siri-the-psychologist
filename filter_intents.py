import json
import pickle

# Load training tags from labels.pkl
with open("labels.pkl", "rb") as f:
    trained_tags = pickle.load(f)

# Load full intents.json
with open("intents.json", "r", encoding="utf-8") as f:
    full_intents = json.load(f)

# Filter intents based on tags used in training
filtered_intents = {
    "intents": [intent for intent in full_intents["intents"] if intent["tag"] in trained_tags]
}

# Save filtered intents to new file
with open("intents_filtered.json", "w", encoding="utf-8") as f:
    json.dump(filtered_intents, f, indent=2)

print(f"[INFO] Saved filtered intents with {len(filtered_intents['intents'])} tags to intents_filtered.json")
