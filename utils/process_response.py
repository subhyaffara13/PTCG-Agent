from typing import List

def process_response(
    input: GeminiEmbeddingInput,
    model_response: EmbeddingResponse,
    model: str,
    _predictions: VertexAIBatchEmbeddingsResponseObject,
) -> EmbeddingResponse:
    openai_embeddings: List[Embedding] = []
    for idx, embedding in enumerate(_predictions["embeddings"]):
        openai_embedding = Embedding(
            embedding=embedding["values"],
            index=idx,
            object="embedding",
        )
        openai_embeddings.append(openai_embedding)

    model_response.data = openai_embeddings
    model_response.model = model

    has_nested = isinstance(input, list) and any(isinstance(e, list) for e in input)
    if _is_multimodal_input(input) or has_nested:
        input_list = input if isinstance(input, list) else [input]
        text_elements: List[str] = []
        for e in input_list:
            if isinstance(e, list):
                text_elements.extend(
                    sub
                    for sub in e
                    if isinstance(sub, str) and not _is_multimodal_element(sub)
                )
            elif isinstance(e, str) and not _is_multimodal_element(e):
                text_elements.append(e)
        if text_elements:
            input_text = get_formatted_prompt(
                data={"input": text_elements}, call_type="embedding"
            )
            prompt_tokens = token_counter(model=model, text=input_text)
        else:
            prompt_tokens = 0
    else:
        input_text = get_formatted_prompt(data={"input": input}, call_type="embedding")
        prompt_tokens = token_counter(model=model, text=input_text)
    model_response.usage = Usage(
        prompt_tokens=prompt_tokens, total_tokens=prompt_tokens
    )

    return model_response

