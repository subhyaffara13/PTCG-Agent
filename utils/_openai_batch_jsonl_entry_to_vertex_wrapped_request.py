from typing import Any, Callable, Dict

def _openai_batch_jsonl_entry_to_vertex_wrapped_request(
    openai_entry: Dict[str, Any],
    map_openai_to_vertex_params: Callable[[Dict[str, Any]], Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Transforms a single OpenAI JSONL batch entry into its Vertex wrapped request.

    jsonl body for vertex is {"request": <request_body>}
    Example Vertex jsonl
    {"request":{"contents": [{"role": "user", "parts": [{"text": "What is the relation between the following video and image samples?"}, {"fileData": {"fileUri": "gs://cloud-samples-data/generative-ai/video/animals.mp4", "mimeType": "video/mp4"}}, {"fileData": {"fileUri": "gs://cloud-samples-data/generative-ai/image/cricket.jpeg", "mimeType": "image/jpeg"}}]}]}}
    """
    openai_request_body = openai_entry.get("body") or {}
    vertex_request_body = _transform_request_body(
        messages=openai_request_body.get("messages", []),
        model=openai_request_body.get("model", ""),
        optional_params=map_openai_to_vertex_params(openai_request_body),
        custom_llm_provider="vertex_ai",
        litellm_params={},
        cached_content=None,
    )

    custom_id = openai_entry.get("custom_id")
    if custom_id is not None:
        if "labels" not in vertex_request_body:
            vertex_request_body["labels"] = {}
        _set_litellm_batch_custom_id_labels(vertex_request_body["labels"], custom_id)

    return {"request": vertex_request_body}

