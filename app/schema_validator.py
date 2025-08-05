# Import the jsonschema library for schema validation
import jsonschema
# Import json to load the schema file
import json

# Load the answer schema JSON from the data folder
with open("../data/answer_schema.json") as f:
    schema = json.load(f)

# Function to validate a given payload (API response) against the schema
def validate_schema(payload):
    jsonschema.validate(instance=payload, schema=schema)
