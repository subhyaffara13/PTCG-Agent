import json

def _extract_old_response(generate_return_json: str) -> str:
    """Pull the model response text out of an old-format generate_returns entry."""
    payload = json.loads(generate_return_json)
    return payload.get("main_response", "")


def _extract_old_response(generate_return_json: str) -> str:
    """Pull the model response text out of an old-format generate_returns entry."""
    payload = json.loads(generate_return_json)
    return payload.get("main_response", "")


def _extract_old_response(generate_return_json: str) -> str:
    """Pull the model response text out of an old-format generate_returns entry."""
    payload = json.loads(generate_return_json)
    return payload.get("main_response", "")

