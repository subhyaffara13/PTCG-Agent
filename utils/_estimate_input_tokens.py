from typing import Any, Dict, Optional

def _estimate_input_tokens(
    request_body: dict,
    route: str,
    model: str,
    model_info: Dict[str, Any],
) -> Optional[int]:
    try:
        if "messages" in request_body:
            return litellm.token_counter(
                model=model,
                messages=request_body.get("messages") or [],
                tools=request_body.get("tools"),
                tool_choice=request_body.get("tool_choice"),
            )
        if "prompt" in request_body:
            return _count_text_tokens(model=model, text=request_body.get("prompt"))
        if "input" in request_body:
            return _count_text_tokens(model=model, text=request_body.get("input"))
        if "query" in request_body or "documents" in request_body:
            query_tokens = _count_text_tokens(
                model=model, text=request_body.get("query")
            )
            document_tokens = _count_text_tokens(
                model=model,
                text=request_body.get("documents"),
            )
            return query_tokens + document_tokens
    except Exception:
        verbose_proxy_logger.debug(
            "Unable to count input tokens for budget reservation", exc_info=True
        )

    max_input_tokens = _to_int(model_info.get("max_input_tokens"))
    if max_input_tokens is not None:
        return max_input_tokens

    return None

