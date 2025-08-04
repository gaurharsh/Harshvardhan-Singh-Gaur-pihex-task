import jsonschema
import json

with open("../data/answer_schema.json") as f:
    schema = json.load(f)

def validate_schema(payload):
    jsonschema.validate(instance=payload, schema=schema)
