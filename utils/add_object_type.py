
def add_object_type(schema):
    # Gemini requires all function parameters to be type OBJECT
    # Handle case where schema has no properties and no type (e.g. tools with no arguments)
    if (
        "type" not in schema
        and "anyOf" not in schema
        and "oneOf" not in schema
        and "allOf" not in schema
    ):
        schema["type"] = "object"

    properties = schema.get("properties", None)
    if properties is not None:
        if "required" in schema and schema["required"] is None:
            schema.pop("required", None)
        # Gemini doesn't accept empty properties for object types
        # If properties is empty, remove it but keep type as object
        if not properties:
            schema.pop("properties", None)
            schema.pop("required", None)
            schema["type"] = "object"
        else:
            schema["type"] = "object"
            for name, value in properties.items():
                add_object_type(value)

    items = schema.get("items", None)
    if items is not None:
        add_object_type(items)

    for key in ["anyOf", "oneOf", "allOf"]:
        values = schema.get(key, None)
        if values is not None and isinstance(values, list):
            for value in values:
                if isinstance(value, dict):
                    add_object_type(value)

