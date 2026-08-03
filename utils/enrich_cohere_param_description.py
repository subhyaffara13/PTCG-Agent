from typing import Any, Dict

def enrich_cohere_param_description(
    description: str, param_schema: Dict[str, Any]
) -> str:
    """Embed schema constraints into a Cohere parameter description.

    ``CohereParameterDefinition`` only has ``type``, ``description``, and
    ``isRequired``.  Rich constraints (``enum``, ``format``, ``minimum``,
    ``maximum``, ``pattern``) are appended to the description string so the
    model can still see and respect them.
    """
    parts = [description] if description else []
    if "enum" in param_schema:
        parts.append(f"Allowed values: {param_schema['enum']}")
    if "format" in param_schema:
        parts.append(f"Format: {param_schema['format']}")
    if "minimum" in param_schema or "maximum" in param_schema:
        range_parts = []
        if "minimum" in param_schema:
            range_parts.append(f"min={param_schema['minimum']}")
        if "maximum" in param_schema:
            range_parts.append(f"max={param_schema['maximum']}")
        parts.append(f"Range: {', '.join(range_parts)}")
    if "pattern" in param_schema:
        parts.append(f"Pattern: {param_schema['pattern']}")
    return ". ".join(parts) if parts else ""

