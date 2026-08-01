
def is_valid_api_key(key: str) -> bool:
    """
    Validates API key format:
    - sk- keys: must match ^sk-[A-Za-z0-9_-]+$
    - hashed keys: must match ^[a-fA-F0-9]{64}$
    - Length between 20 and 100 characters
    """
    import re

    if not isinstance(key, str):
        return False
    if 3 <= len(key) <= 100:
        if re.match(r"^sk-[A-Za-z0-9_-]+$", key):
            return True
        if re.match(r"^[a-fA-F0-9]{64}$", key):
            return True
    return False

