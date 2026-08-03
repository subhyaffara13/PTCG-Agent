from typing import Any, Dict

def _get_litellm_batch_custom_id_from_labels(labels: Dict[str, Any]) -> str:
    """Prefer encoded custom_id when present (see _set_litellm_batch_custom_id_labels)."""
    raw = labels.get("litellm_custom_id_raw")
    if raw:
        raw_chunks = [str(raw)]
        chunk_prefix = "litellm_custom_id_raw_"
        indexed_chunks = []
        for key, value in labels.items():
            if key.startswith(chunk_prefix) and key[len(chunk_prefix) :].isdigit():
                indexed_chunks.append((int(key[len(chunk_prefix) :]), str(value)))
        raw_chunks.extend(
            raw_label_chunk
            for _, raw_label_chunk in sorted(indexed_chunks, key=lambda item: item[0])
        )
        decoded = _decode_gcp_label_value_chunks(raw_chunks)
        if decoded is not None:
            return decoded
        return str(raw)
    return str(labels.get("litellm_custom_id", "unknown"))

