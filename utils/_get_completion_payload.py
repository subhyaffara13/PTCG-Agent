
def _get_completion_payload(response_headers: list[dict], oid: str) -> CompletionPayloadT:
    parts: list[PayloadPartT] = []
    for part_number, header in enumerate(response_headers):
        etag = header.get("etag")
        if etag is None or etag == "":
            raise ValueError(f"Invalid etag (`{etag}`) returned for part {part_number + 1}")
        parts.append(
            {
                "partNumber": part_number + 1,
                "etag": etag,
            }
        )
    return {"oid": oid, "parts": parts}

