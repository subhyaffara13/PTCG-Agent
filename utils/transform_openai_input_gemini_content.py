
def transform_openai_input_gemini_content(
    input: GeminiEmbeddingInput,
    model: str,
    optional_params: dict,
    resolved_files: Optional[Dict[str, Dict[str, str]]] = None,
) -> VertexAIBatchEmbeddingsRequestBody:
    """
    Transform OpenAI embedding input to Gemini batchEmbedContents format.

    Each input element becomes a separate EmbedContentRequest, supporting
    text, data URIs, file references, and GCS URLs.

    If an element is a list (nested input), all sub-elements are combined
    into a single content with multiple parts, producing one combined
    embedding for the group.

    Examples:
        input=["text", "image"]         → 2 separate embeddings
        input=[["text", "image"]]       → 1 combined embedding
        input=[["text", "image"], "x"]  → 2 embeddings (1 combined + 1 separate)
    """
    gemini_model_name = "models/{}".format(model)

    gemini_params = _filter_embed_params(optional_params)

    input_list = [input] if isinstance(input, str) else input
    requests: List[EmbedContentRequest] = []

    for element in input_list:
        if isinstance(element, list):
            if not element:
                raise ValueError("Nested input list must not be empty")
            for sub in element:
                if not isinstance(sub, str):
                    raise ValueError(
                        f"Elements inside a nested input list must be strings, got {type(sub)}"
                    )
            parts = [
                _build_part_for_input(sub, resolved_files=resolved_files)
                for sub in element
            ]
        else:
            parts = [_build_part_for_input(element, resolved_files=resolved_files)]
        request = EmbedContentRequest(
            model=gemini_model_name,
            content=ContentType(parts=parts),
            **gemini_params,
        )
        requests.append(request)

    return VertexAIBatchEmbeddingsRequestBody(requests=requests)

