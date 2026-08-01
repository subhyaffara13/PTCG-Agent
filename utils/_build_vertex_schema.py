
def _build_vertex_schema(parameters: dict, add_property_ordering: bool = False):
    """
    This is a modified version of https://github.com/google-gemini/generative-ai-python/blob/8f77cc6ac99937cd3a81299ecf79608b91b06bbb/google/generativeai/types/content_types.py#L419

    Updates the input parameters, removing extraneous fields, adjusting types, unwinding $defs, and adding propertyOrdering if specified, returning the updated parameters.

    Parameters:
        parameters: dict - the json schema to build from
        add_property_ordering: bool - whether to add propertyOrdering to the schema. This is only applicable to schemas for structured outputs. See
          set_schema_property_ordering for more details.
    Returns:
        parameters: dict - the input parameters, modified in place
    """
    # Get valid fields from Schema TypedDict
    valid_schema_fields = set(get_type_hints(Schema).keys())

    defs = parameters.pop("$defs", {})
    # Expand $ref references in parameters using the definitions
    # Note: We don't pre-flatten defs as that causes exponential memory growth
    # with circular references (see issue #19098). unpack_defs handles nested
    # refs recursively and correctly detects/skips circular references.
    unpack_defs(parameters, defs)

    # 5. Nullable fields:
    #     * https://github.com/pydantic/pydantic/issues/1270
    #     * https://stackoverflow.com/a/58841311
    #     * https://github.com/pydantic/pydantic/discussions/4872
    convert_anyof_null_to_nullable(parameters)

    _convert_schema_types(parameters)

    # Handle empty strings in enum values - Gemini doesn't accept empty strings in enums
    _fix_enum_empty_strings(parameters)

    # Remove enums for non-string typed fields (Gemini requires enum only on strings)
    _fix_enum_types(parameters)

    # Handle empty items objects
    process_items(parameters)
    add_object_type(parameters)
    # Postprocessing
    # Filter out fields that don't exist in Schema

    parameters = filter_schema_fields(parameters, valid_schema_fields)

    if add_property_ordering:
        set_schema_property_ordering(parameters)

    return parameters

