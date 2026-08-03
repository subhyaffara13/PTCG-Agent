import json

def _extract_old_prompt(generate_return_json: str) -> str:
    """Pull the user prompt text out of an old-format generate_returns entry."""
    payload = json.loads(generate_return_json)
    messages = payload["request_for_logging"]["messages"]
    return messages[0]["content"][0]["text"]


def _extract_old_prompt(generate_return_json: str) -> str:
    """Pull the user prompt text out of an old-format generate_returns entry."""
    payload = json.loads(generate_return_json)
    messages = payload["request_for_logging"]["messages"]
    # The harness sent a single user message with one text content block.
    return messages[0]["content"][0]["text"]


def _extract_old_prompt(generate_return_json: str) -> str:
    """Pull the user prompt text out of an old-format generate_returns entry."""
    payload = json.loads(generate_return_json)
    messages = payload["request_for_logging"]["messages"]
    # The harness sent a single user message with one text content block.
    return messages[0]["content"][0]["text"]

