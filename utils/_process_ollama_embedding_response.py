from typing import Any, List

def _process_ollama_embedding_response(
    response_json: dict,
    prompts: List[str],
    model: str,
    model_response: EmbeddingResponse,
    logging_obj: Any,
    encoding: Any,
) -> EmbeddingResponse:
    output_data = []
    embeddings: List[List[float]] = response_json["embeddings"]

    for idx, emb in enumerate(embeddings):
        output_data.append({"object": "embedding", "index": idx, "embedding": emb})

    input_tokens = response_json.get("prompt_eval_count", None)

    if input_tokens is None:
        if encoding is not None:
            input_tokens = len(encoding.encode("".join(prompts)))
            if logging_obj:
                logging_obj.debug(
                    "Ollama response missing prompt_eval_count; estimated with encoding."
                )
        else:
            input_tokens = 0
            if logging_obj:
                logging_obj.warning(
                    "Missing prompt_eval_count and no encoding provided; defaulted to 0."
                )

    model_response.object = "list"
    model_response.data = output_data
    model_response.model = "ollama/" + model
    model_response.usage = litellm.Usage(
        prompt_tokens=input_tokens,
        completion_tokens=0,
        total_tokens=input_tokens,
        prompt_tokens_details=None,
        completion_tokens_details=None,
    )
    return model_response

