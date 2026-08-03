import json

def is_valid_json(value: str) -> bool:
    """Checks whether the value passed is a valid serialized JSON string"""
    try:
        json.loads(value)
    except json.JSONDecodeError:
        return False
    else:
        return True

