from typing import Any, Dict

def set_schema_property_ordering(
    schema: Dict[str, Any], depth: int = 0
) -> Dict[str, Any]:
    """
    vertex ai and generativeai apis order output of fields alphabetically, unless you specify the order.
    python dicts retain order, so we just use that. Note that this field only applies to structured outputs, and not tools.
    Function tools are not afflicted by the same alphabetical ordering issue, (the order of keys returned seems to be arbitrary, up to the model)
    https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.cachedContents#Schema.FIELDS.property_ordering

    Args:
        schema: The schema dictionary to process
        depth: Current recursion depth to prevent infinite loops
    """
    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        raise ValueError(
            f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while processing schema. Please check the schema for excessive nesting."
        )

    if "properties" in schema and isinstance(schema["properties"], dict):
        # retain propertyOrdering as an escape hatch if user already specifies it
        if "propertyOrdering" not in schema:
            schema["propertyOrdering"] = [k for k, v in schema["properties"].items()]
        for k, v in schema["properties"].items():
            set_schema_property_ordering(v, depth + 1)
    if "items" in schema:
        set_schema_property_ordering(schema["items"], depth + 1)
    return schema

