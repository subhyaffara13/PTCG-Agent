from typing import Any, List, Tuple

def _truncate_evidence_payload(
    evidence: Any, max_bytes: int = MAX_PILLAR_HEADER_VALUE_BYTES
) -> Tuple[Any, str, bool]:
    """
    Truncate evidence payload so the encoded header value stays within max_bytes.

    Returns:
        truncated_evidence: Evidence list/value after truncation
        encoded_value: URL-encoded JSON string for header
        was_truncated: Whether truncation occurred
    """
    if not isinstance(evidence, list):
        encoded = _encode_json_for_header(evidence)
        if len(encoded.encode("utf-8")) <= max_bytes:
            return evidence, encoded, False
        truncated_value = "[truncated]"
        return truncated_value, _encode_json_for_header(truncated_value), True

    truncated: List[Any] = []
    encoded = _encode_json_for_header(truncated)
    truncated_flag = False

    for entry in evidence:
        working_entry: Any
        if isinstance(entry, dict):
            working_entry = dict(entry)
        else:
            working_entry = entry

        truncated.append(working_entry)
        encoded = _encode_json_for_header(truncated)

        if len(encoded.encode("utf-8")) <= max_bytes:
            continue

        truncated_flag = True
        if isinstance(working_entry, dict):
            evidence_text = str(working_entry.get("evidence", ""))
            if evidence_text:
                step = max(1, len(evidence_text) // 2)
                while len(encoded.encode("utf-8")) > max_bytes and evidence_text:
                    evidence_text = (
                        evidence_text[:-step]
                        if len(evidence_text) > step
                        else evidence_text[:-1]
                    )
                    step = max(1, step // 2)
                    truncated_text = (
                        f"{evidence_text}...[truncated]"
                        if evidence_text
                        else "[truncated]"
                    )
                    working_entry["evidence"] = truncated_text
                    working_entry["evidence_truncated"] = True
                    encoded = _encode_json_for_header(truncated)

                if len(encoded.encode("utf-8")) <= max_bytes:
                    continue

        truncated.pop()
        encoded = _encode_json_for_header(truncated)

    return truncated, encoded, truncated_flag

