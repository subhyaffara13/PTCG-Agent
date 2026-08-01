
def preserve_upstream_non_openai_attributes(
    model_response: "ModelResponseStream", original_chunk: "ModelResponseStream"
):
    """
    Preserve non-OpenAI attributes from the original chunk.
    """
    # Access model_fields on the class, not the instance, to avoid Pydantic 2.11+ deprecation warnings
    expected_keys = set(type(model_response).model_fields.keys()).union({"usage"})
    for key, value in original_chunk.model_dump().items():
        if key not in expected_keys:
            setattr(model_response, key, value)

