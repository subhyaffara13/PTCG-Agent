from typing import Any, Dict, List

def _convert_schema_types(schema, depth=0):
    """
    Convert type arrays and lowercase types for Vertex AI compatibility.

    Transforms OpenAI-style schemas to Vertex AI format by converting type arrays
    like ["string", "number"] to anyOf format and converting all types to uppercase.
    """
    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        raise ValueError(
            f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while processing schema. Please check the schema for excessive nesting."
        )

    if not isinstance(schema, dict):
        return

    # Handle type field
    if "type" in schema:
        type_val = schema["type"]
        if isinstance(type_val, list) and len(type_val) > 1:
            # Convert type arrays to anyOf format
            # Fields that are specific to object/array types and should move into anyOf
            type_specific_fields = {
                "properties",
                "required",
                "additionalProperties",
                "items",
                "minItems",
                "maxItems",
                "minProperties",
                "maxProperties",
            }

            any_of: List[Dict[str, Any]] = []
            for t in type_val:
                if not isinstance(t, str):
                    continue
                if t == "null":
                    # Keep null entry minimal so we can strip it later.
                    any_of.append({"type": "null"})
                    continue

                # For object/array types, include type-specific fields
                if t in ("object", "array"):
                    item_schema = {"type": t}
                    # Move type-specific fields into this anyOf item
                    for field in type_specific_fields:
                        if field in schema:
                            item_schema[field] = deepcopy(schema[field])
                    any_of.append(item_schema)
                else:
                    # For primitive types, only include the type
                    any_of.append({"type": t})

            # Remove type-specific fields from parent if we moved them into anyOf
            has_object_or_array = any(
                t in ("object", "array") for t in type_val if isinstance(t, str)
            )
            if has_object_or_array:
                for field in type_specific_fields:
                    schema.pop(field, None)

            schema["anyOf"] = any_of
            schema.pop("type")
        elif isinstance(type_val, list) and len(type_val) == 1:
            schema["type"] = type_val[0]
        elif isinstance(type_val, str):
            schema["type"] = type_val

    # Recursively process nested properties, items, and anyOf
    for key in ["properties", "items", "anyOf"]:
        if key in schema:
            value = schema[key]
            if key == "properties" and isinstance(value, dict):
                for prop_schema in value.values():
                    _convert_schema_types(prop_schema, depth + 1)
            elif key == "items":
                _convert_schema_types(value, depth + 1)
            elif key == "anyOf" and isinstance(value, list):
                for anyof_schema in value:
                    _convert_schema_types(anyof_schema, depth + 1)

