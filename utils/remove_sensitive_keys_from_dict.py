
def remove_sensitive_keys_from_dict(d: dict) -> dict:
    """
    Remove sensitive keys from a dictionary
    """
    sensitive_key_phrases = ["key", "secret", "access", "credential"]
    remove_keys = []
    for key in d.keys():
        if any(phrase in key.lower() for phrase in sensitive_key_phrases):
            remove_keys.append(key)
    for key in remove_keys:
        d.pop(key)
    return d

