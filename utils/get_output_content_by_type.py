
def get_output_content_by_type(
    response_obj: Union[
        None,
        dict,
        EmbeddingResponse,
        ModelResponse,
        TextCompletionResponse,
        ImageResponse,
        TranscriptionResponse,
        RerankResponse,
        HttpxBinaryResponseContent,
        ResponsesAPIResponse,
        list,
    ],
    kwargs: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Extract output content from response objects based on their type.

    This utility function handles the type-specific logic for converting
    various response objects into appropriate output formats for Langfuse logging.

    Args:
        response_obj: The response object returned by the function
        kwargs: Optional keyword arguments containing call_type and other metadata

    Returns:
        The formatted output content suitable for Langfuse logging, or None
    """
    if response_obj is None:
        return ""

    kwargs = kwargs or {}
    call_type = kwargs.get("call_type", None)

    # Embedding responses - no output content
    if call_type == "embedding" or isinstance(response_obj, EmbeddingResponse):
        return "embedding-output"

    # Binary/Speech responses
    if isinstance(response_obj, HttpxBinaryResponseContent):
        return "speech-output"

    if isinstance(response_obj, BaseModel):
        return response_obj.model_dump_json()

    if response_obj and (
        isinstance(response_obj, dict) or isinstance(response_obj, list)
    ):
        return json.dumps(response_obj)
    else:
        return ""

