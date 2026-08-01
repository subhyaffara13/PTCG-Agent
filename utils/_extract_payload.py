
def _extract_payload(response: str) -> dict[str, Any] | None:
    """Pull the LAST JSON object that carries a negotiation action field."""
    return extract_last_json_object(response, required_keys=_PAYLOAD_KEYS)

