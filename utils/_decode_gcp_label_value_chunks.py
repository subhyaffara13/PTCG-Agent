from typing import List, Optional

def _decode_gcp_label_value_chunks(values: List[str]) -> Optional[str]:
    """Decode values produced by _encode_gcp_label_value_chunks."""
    encoded_parts = []
    for value in values:
        if not value.startswith(_CUSTOM_ID_RAW_LABEL_PREFIX):
            return None
        encoded_parts.append(value[len(_CUSTOM_ID_RAW_LABEL_PREFIX) :])
    encoded = "".join(encoded_parts).upper()
    padding = "=" * (-len(encoded) % 8)
    try:
        return base64.b32decode(encoded + padding).decode("utf-8")
    except Exception:
        return None

