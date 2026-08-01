
def _build_json_schema(parameters: dict) -> dict:
    """
    Build a JSON Schema for use with Gemini's responseJsonSchema parameter.

    Unlike _build_vertex_schema (used for responseSchema), this function:
    - Does NOT convert types to uppercase (keeps standard JSON Schema format)
    - Does NOT add propertyOrdering
    - Does NOT filter fields (allows additionalProperties)
    - Preserves $defs/$ref (Gemini 2.0+ supports JSON Schema references natively)

    Parameters:
        parameters: dict - the JSON schema to process

    Returns:
        dict - the processed schema in standard JSON Schema format
    """
    # Gemini 2.0+ with responseJsonSchema accepts standard JSON Schema as-is,
    # including $ref, $defs, anyOf, etc. No transformations needed — the
    # OpenAPI-specific fixes (unpack_defs, add_object_type, convert_anyof, etc.)
    # are only required for responseSchema (Gemini 1.5) and can break valid
    # JSON Schema by adding conflicting fields to $ref nodes.
    # See: https://blog.google/technology/developers/gemini-api-structured-outputs/

    return parameters

