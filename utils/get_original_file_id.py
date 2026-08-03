import re

def get_original_file_id(encoded_id: str) -> str:
    """
    Extract the original provider file/batch ID from an encoded ID.
    Handles IDs that start with "file-" or "batch_" prefix.
    """
    try:
        if not isinstance(encoded_id, str):
            return encoded_id

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
            match = re.search(r"litellm:([^;]+);model,", decoded)
            if match:
                return match.group(1)

        return encoded_id
    except Exception:
        return encoded_id

