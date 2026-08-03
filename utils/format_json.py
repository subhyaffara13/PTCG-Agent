import json

def format_json(blob: str):
    parsed = json.loads(blob)
    return json.dumps(parsed, indent=2)

