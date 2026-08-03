from typing import Any, Optional

def safe_deep_copy(data):
    """
    Safe Deep Copy

    The LiteLLM request may contain objects that cannot be pickled/deep-copied
    (e.g., tracing spans, locks, clients).

    This helper deep-copies each top-level key independently; on failure keeps
    original ref
    """
    import copy

    import litellm

    if litellm.safe_memory_mode is True:
        return data

    litellm_parent_otel_span: Optional[Any] = None
    # Step 1: Remove the litellm_parent_otel_span
    litellm_parent_otel_span = None
    if isinstance(data, dict):
        # remove litellm_parent_otel_span since this is not picklable
        if "metadata" in data and "litellm_parent_otel_span" in data["metadata"]:
            litellm_parent_otel_span = data["metadata"].pop("litellm_parent_otel_span")
            data["metadata"]["litellm_parent_otel_span"] = "placeholder"
        if (
            "litellm_metadata" in data
            and "litellm_parent_otel_span" in data["litellm_metadata"]
        ):
            litellm_parent_otel_span = data["litellm_metadata"].pop(
                "litellm_parent_otel_span"
            )
            data["litellm_metadata"]["litellm_parent_otel_span"] = "placeholder"

    # Step 2: Per-key deepcopy with fallback
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            try:
                new_data[k] = copy.deepcopy(v)
            except Exception:
                new_data[k] = v
    else:
        try:
            new_data = copy.deepcopy(data)
        except Exception:
            new_data = data

    # Step 3: re-add the litellm_parent_otel_span after doing a deep copy
    if isinstance(data, dict) and litellm_parent_otel_span is not None:
        if "metadata" in data and "litellm_parent_otel_span" in data["metadata"]:
            data["metadata"]["litellm_parent_otel_span"] = litellm_parent_otel_span
        if (
            "litellm_metadata" in data
            and "litellm_parent_otel_span" in data["litellm_metadata"]
        ):
            data["litellm_metadata"][
                "litellm_parent_otel_span"
            ] = litellm_parent_otel_span
    return new_data

