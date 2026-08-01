
def _synthesize_oci_tool_call_id(position: int, name: str, arguments: str) -> str:
    """Deterministic synthetic tool-call id derived from chunk content.

    Used as a fallback when OCI omits ``id`` (always the case for the OCI
    Cohere protocol, occasionally the case for OCI GENERIC streaming chunks).
    A random ``uuid4`` per chunk would cause downstream stream-merging
    consumers — which key off the tool-call ``id`` — to treat re-emissions of
    the same logical call (e.g. terminal consolidation chunks, retries) as
    distinct calls. A content-derived digest stays stable across identical
    re-emissions while differing across truly distinct calls.
    """
    digest = hashlib.sha256(
        f"{position}|{name}|{arguments}".encode("utf-8"),
        usedforsecurity=False,
    ).hexdigest()[:24]
    return f"call_{digest}"

