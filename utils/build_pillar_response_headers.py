
def build_pillar_response_headers(metadata_store: Dict[str, Any]) -> Dict[str, str]:
    """
    Create URL-safe Pillar response headers and apply truncation metadata.
    """
    headers: Dict[str, str] = {}

    if "pillar_flagged" in metadata_store:
        headers["x-pillar-flagged"] = str(metadata_store["pillar_flagged"]).lower()

    if "pillar_scanners" in metadata_store:
        headers["x-pillar-scanners"] = _encode_json_for_header(
            metadata_store["pillar_scanners"]
        )

    if "pillar_evidence" in metadata_store:
        truncated_evidence, encoded_value, truncated_flag = _truncate_evidence_payload(
            metadata_store["pillar_evidence"]
        )
        metadata_store["pillar_evidence"] = truncated_evidence
        if truncated_flag:
            metadata_store["pillar_evidence_truncated"] = True
        headers["x-pillar-evidence"] = encoded_value

    if "pillar_session_id_response" in metadata_store:
        headers["x-pillar-session-id"] = quote(
            str(metadata_store["pillar_session_id_response"]), safe=""
        )

    if headers:
        metadata_store["pillar_response_headers"] = headers
        metadata_store[TRUSTED_PILLAR_RESPONSE_HEADERS_METADATA_KEY] = True

    return headers

