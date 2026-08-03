import json
from typing import Any

def generate_hash_from_response(response_obj: Any) -> str:
    """
    Generate a stable hash from a response object.

    Args:
        response_obj: The response object to hash (can be dict, list, etc.)

    Returns:
        A hex string representation of the MD5 hash
    """
    try:
        # Create a stable JSON string of the entire response object
        # Sort keys to ensure consistent ordering
        json_str = json.dumps(response_obj, sort_keys=True)

        # Generate a hash of the response object
        unique_hash = hashlib.md5(json_str.encode()).hexdigest()
        return unique_hash
    except Exception:
        # Return a fallback hash if serialization fails
        return hashlib.md5(str(response_obj).encode()).hexdigest()

