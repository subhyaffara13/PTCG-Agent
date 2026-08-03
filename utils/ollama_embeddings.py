from typing import Any, List

def ollama_embeddings(
    api_base: str,
    model: str,
    prompts: List[str],
    optional_params: dict,
    model_response: EmbeddingResponse,
    logging_obj: Any,
    encoding: Any = None,
):
    if not api_base.endswith("/api/embed"):
        api_base += "/api/embed"

    data = _prepare_ollama_embedding_payload(model, prompts, optional_params)

    response = litellm.module_level_client.post(url=api_base, json=data)
    response_json = response.json()

    return _process_ollama_embedding_response(
        response_json=response_json,
        prompts=prompts,
        model=model,
        model_response=model_response,
        logging_obj=logging_obj,
        encoding=encoding,
    )

