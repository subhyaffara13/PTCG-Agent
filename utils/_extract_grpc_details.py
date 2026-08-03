from typing import Any, Optional

def _extract_grpc_details(error: Any) -> Optional[str]:
    """Best-effort extraction of a human-readable detail string from a gRPC error."""
    details_fn = getattr(error, "details", None)
    if callable(details_fn):
        try:
            details = details_fn()
        except Exception:
            details = None
        if isinstance(details, str) and details:
            return details
    return None

