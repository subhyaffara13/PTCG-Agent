
def transform_openai_input_gemini_embed_content(
    input: GeminiEmbeddingInput,
    model: str,
    optional_params: dict,
    resolved_files: Optional[Dict[str, Dict[str, str]]] = None,
) -> dict:
    """
    Transform OpenAI embedding input to Gemini embedContent format (multimodal).

    Args:
        input: GeminiEmbeddingInput with text, data URIs, or file references
        model: Model name
        optional_params: Additional parameters (taskType, outputDimensionality, etc.)
        resolved_files: Dict mapping file names (files/abc) to {mime_type, uri}

    Returns:
        dict: Gemini embedContent request body with content.parts
    """
    resolved_files = resolved_files or {}

    gemini_params = _filter_embed_params(optional_params)

    input_list = [input] if isinstance(input, str) else input
    parts: List[PartType] = []

    for element in input_list:
        if isinstance(element, list):
            raise ValueError(
                "Nested (combined) embeddings are not supported on the embedContent path. "
                "Use the batchEmbedContents path or pass a flat list instead."
            )
        if not isinstance(element, str):
            raise ValueError(f"Unsupported input type: {type(element)}")
        parts.append(_build_part_for_input(element, resolved_files=resolved_files))

    request_body: dict = {
        "content": ContentType(parts=parts),
        **gemini_params,
    }

    return request_body

