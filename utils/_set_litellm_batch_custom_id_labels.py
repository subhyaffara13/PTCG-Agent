
def _set_litellm_batch_custom_id_labels(labels: Dict[str, str], custom_id: Any) -> None:
    """
    Store OpenAI batch custom_id for Vertex batch correlation.

    ``litellm_custom_id`` is GCP-label-safe (may alter casing and characters).
    ``litellm_custom_id_raw`` encodes the original string for
    round-trip correlation in batch output transforms.
    """
    custom_id_str = str(custom_id)
    labels["litellm_custom_id"] = _sanitize_gcp_label_value(custom_id_str)
    raw_label_chunks = _encode_gcp_label_value_chunks(custom_id_str)
    labels["litellm_custom_id_raw"] = raw_label_chunks[0]
    for index, raw_label_chunk in enumerate(raw_label_chunks[1:], start=1):
        labels[f"litellm_custom_id_raw_{index}"] = raw_label_chunk

