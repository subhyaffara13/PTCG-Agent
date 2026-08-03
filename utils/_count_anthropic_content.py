from typing import Any, Optional

def _count_anthropic_content(
    content: Mapping[str, Any],
    count_function: TokenCounterFunction,
    use_default_image_token_count: bool,
    default_token_count: Optional[int],
) -> int:
    """
    Count tokens in Anthropic-specific content blocks (tool_use, tool_result, etc.).

    Uses TypedDict definitions from litellm.types.llms.anthropic to determine
    what fields to count and how to handle nested structures.

    Dynamically infers which fields to count based on the TypedDict definition,
    avoiding hardcoded field names.
    """
    typeddict_cls = _validate_anthropic_content(content)
    type_hints = getattr(typeddict_cls, "__annotations__", {})
    tokens = 0

    # Fields to skip (metadata/identifiers that don't contribute to prompt tokens)
    skip_fields = {"type", "id", "tool_use_id", "cache_control", "is_error"}

    # Iterate over all fields defined in the TypedDict
    for field_name, field_type in type_hints.items():
        if field_name in skip_fields:
            continue

        field_value = content.get(field_name)
        if field_value is None:
            continue
        try:
            if isinstance(field_value, str):
                tokens += count_function(field_value)
            elif isinstance(field_value, list):
                tokens += _count_content_list(
                    count_function,
                    field_value,  # type: ignore
                    use_default_image_token_count,
                    default_token_count,
                )
            elif isinstance(field_value, dict):
                tokens += count_function(str(field_value))
        except Exception as e:
            if default_token_count is not None:
                return default_token_count
            raise ValueError(f"Error counting field '{field_name}': {e}")
    return tokens

