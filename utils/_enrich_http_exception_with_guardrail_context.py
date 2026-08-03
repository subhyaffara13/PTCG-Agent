from typing import Any

def _enrich_http_exception_with_guardrail_context(
    exc: BaseException, callback: Any
) -> None:
    """
    If `exc` is an HTTPException with a dict `detail`, mutate it in place to
    add `guardrail_name` and `guardrail_mode` taken from the callback instance.

    Uses setdefault so guardrails that already populate these fields explicitly
    win over the inferred defaults. No-op for non-HTTPException, non-dict-detail,
    or callbacks without `guardrail_name`. Never raises.
    """
    if not isinstance(exc, HTTPException):
        return
    detail = getattr(exc, "detail", None)
    if not isinstance(detail, dict):
        return
    guardrail_name = getattr(callback, "guardrail_name", None)
    if guardrail_name:
        detail.setdefault("guardrail_name", guardrail_name)
    event_hook = getattr(callback, "event_hook", None)
    if event_hook:
        detail.setdefault("guardrail_mode", event_hook)

