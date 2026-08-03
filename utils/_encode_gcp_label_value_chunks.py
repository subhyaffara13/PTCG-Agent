from typing import List

def _encode_gcp_label_value_chunks(value: str) -> List[str]:
    """Encode arbitrary text across one or more GCP-label-safe values."""
    max_encoded_len = _GCP_LABEL_VALUE_MAX_LEN - len(_CUSTOM_ID_RAW_LABEL_PREFIX)
    encoded = (
        base64.b32encode(value.encode("utf-8")).decode("ascii").rstrip("=").lower()
    )
    return [
        f"{_CUSTOM_ID_RAW_LABEL_PREFIX}{encoded[i : i + max_encoded_len]}"
        for i in range(0, len(encoded), max_encoded_len)
    ] or [_CUSTOM_ID_RAW_LABEL_PREFIX]

