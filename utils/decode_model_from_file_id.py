import re
from typing import Optional

def decode_model_from_file_id(encoded_id: str) -> Optional[str]:
    """
    Extract model name from an encoded file/batch ID.
    Handles IDs that start with "file-" or "batch_" prefix.
    """
    try:
        if not isinstance(encoded_id, str):
            return None

        # Remove prefix if present (file-, batch_, etc.)
        if encoded_id.startswith("file-"):
            b64_part = encoded_id[5:]  # Remove "file-"
        elif encoded_id.startswith("batch_"):
            b64_part = encoded_id[6:]  # Remove "batch_"
        else:
            b64_part = encoded_id

        padded = b64_part + "=" * (-len(b64_part) % 4)
        decoded = base64.urlsafe_b64decode(padded).decode()
        if decoded.startswith("litellm:") and ";model," in decoded:
            match = re.search(r";model,([^;]+)", decoded)
            if match:
                return match.group(1).strip()

        return None
    except Exception:
        return None

