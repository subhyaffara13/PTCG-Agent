import re

def is_model_allowed_by_pattern(model: str, allowed_model_pattern: str) -> bool:
    """
    Check if a model matches an allowed pattern.
    Handles exact matches and wildcard patterns.

    Args:
        model (str): The model to check (e.g., "bedrock/anthropic.claude-3-5-sonnet-20240620")
        allowed_model_pattern (str): The allowed pattern (e.g., "bedrock/*", "*", "openai/*")

    Returns:
        bool: True if model matches the pattern, False otherwise
    """
    if "*" in allowed_model_pattern:
        pattern = f"^{allowed_model_pattern.replace('*', '.*')}$"
        return bool(re.match(pattern, model))

    return False

