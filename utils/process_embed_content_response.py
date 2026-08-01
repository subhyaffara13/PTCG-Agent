
def process_embed_content_response(
    input: GeminiEmbeddingInput,
    model_response: EmbeddingResponse,
    model: str,
    response_json: dict,
) -> EmbeddingResponse:
    """
    Process Gemini embedContent response (single embedding for multimodal input).

    Args:
        input: Original input
        model_response: EmbeddingResponse to populate
        model: Model name
        response_json: Raw JSON response from embedContent endpoint

    Returns:
        EmbeddingResponse with single embedding
    """
    if "embedding" not in response_json:
        raise ValueError(
            f"embedContent response missing 'embedding' field: {response_json}"
        )

    embedding_data = response_json["embedding"]

    openai_embedding = Embedding(
        embedding=embedding_data["values"],
        index=0,
        object="embedding",
    )

    model_response.data = [openai_embedding]
    model_response.model = model

    if _is_multimodal_input(input):
        prompt_tokens = 0
    else:
        input_text = get_formatted_prompt(data={"input": input}, call_type="embedding")
        prompt_tokens = token_counter(model=model, text=input_text)
    model_response.usage = Usage(
        prompt_tokens=prompt_tokens, total_tokens=prompt_tokens
    )

    return model_response

