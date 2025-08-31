# oneline.py
import json

# Make sure your key file is named 'service-account.json'
# and is in the same folder as this script.
with open('service-account.json', 'r') as f:
    data = json.load(f)

# This will print the entire file as a perfect, single-line JSON string
print(json.dumps(data))