import re

def _fuzzy_match_size(config_name: str) -> str | None:
    """
    Extract the size digit from torchao config class names like "Int4WeightOnlyConfig", "Int8WeightOnlyConfig".
    Returns the digit as a string if found, otherwise None.
    """
    match = re.search(r"(\d)weight", config_name.lower())
    return match.group(1) if match else None

