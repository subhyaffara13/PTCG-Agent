from typing import Any

def _get_guardrail_attrs(g: Any) -> tuple[Any, str]:
    """Get (guardrail_id, display_name) from guardrail - handles Prisma model or dict."""
    gid = getattr(g, "guardrail_id", None) or (
        g.get("guardrail_id") if isinstance(g, dict) else None
    )
    name = getattr(g, "guardrail_name", None) or (
        g.get("guardrail_name") if isinstance(g, dict) else None
    )
    return gid, (name or gid or "")

