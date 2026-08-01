
def convert_anyof_null_to_nullable(schema, depth=0):
    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        raise ValueError(
            f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while processing schema. Please check the schema for excessive nesting."
        )
    """ Converts null objects within anyOf by removing them and adding nullable to all remaining objects """
    anyof = schema.get("anyOf", None)
    if anyof is not None:
        contains_null = False
        for atype in anyof:
            if isinstance(atype, dict) and atype.get("type") == "null":
                # remove null type
                anyof.remove(atype)
                contains_null = True
            elif "type" not in atype and len(atype) == 0:
                # Handle empty object case
                atype["type"] = "object"

        if len(anyof) == 0:
            # Edge case: response schema with only null type present is invalid in Vertex AI
            raise ValueError(
                "Invalid input: AnyOf schema with only null type is not supported. "
                "Please provide a non-null type."
            )

        if contains_null:
            # set all types to nullable following guidance found here: https://cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-gemini-controlled-generation-response-schema-3#generativeaionvertexai_gemini_controlled_generation_response_schema_3-python
            # Empty `items: {}` on array branches is left in place; downstream
            # process_items() converts it to {"type": "object"}, which Vertex
            # requires whenever type == "array" (even inside anyOf).
            for atype in anyof:
                atype["nullable"] = True

    properties = schema.get("properties", None)
    if properties is not None:
        for name, value in properties.items():
            convert_anyof_null_to_nullable(value, depth=depth + 1)

    items = schema.get("items", None)
    if items is not None:
        convert_anyof_null_to_nullable(items, depth=depth + 1)

