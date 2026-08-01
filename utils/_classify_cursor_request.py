
def _classify_cursor_request(method: str, path: str) -> str:
    """Classify a Cursor API request into a readable operation name."""
    normalized = path.rstrip("/")

    for pattern, operation in CURSOR_AGENT_ENDPOINTS.items():
        pat_method, pat_path = pattern.split(" ", 1)
        if method.upper() != pat_method:
            continue

        pat_parts = pat_path.strip("/").split("/")
        req_parts = normalized.strip("/").split("/")

        if len(pat_parts) != len(req_parts):
            continue

        match = True
        for pp, rp in zip(pat_parts, req_parts):
            if pp.startswith("{") and pp.endswith("}"):
                continue
            if pp != rp:
                match = False
                break
        if match:
            return operation

    return f"cursor:{method.lower()}:{normalized}"

