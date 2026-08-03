from typing import Any

def _merge_guardrails_with_existing(data: dict, model_level_guardrails: Any) -> dict:
    """
    Merge model-level guardrails with any existing guardrails in the request data.

    Args:
        data: The request data dict
        model_level_guardrails: Guardrails defined at the model level

    Returns:
        Modified data dict with merged guardrails in metadata
    """
    modified_data = data.copy()
    metadata = modified_data.setdefault("metadata", {})
    existing_guardrails = metadata.get("guardrails", [])

    # Ensure existing_guardrails is a list
    if not isinstance(existing_guardrails, list):
        existing_guardrails = [existing_guardrails] if existing_guardrails else []

    # Ensure model_level_guardrails is a list
    if not isinstance(model_level_guardrails, list):
        model_level_guardrails = (
            [model_level_guardrails] if model_level_guardrails else []
        )

    # Combine existing and model-level guardrails
    metadata["guardrails"] = list(set(existing_guardrails + model_level_guardrails))
    return modified_data

