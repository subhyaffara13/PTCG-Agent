import json

def _normalize_content(raw: object) -> str | list[_ContentPart] | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        return raw
    if not isinstance(raw, list):
        return json.dumps(raw)
    parts: list[_ContentPart] = []
    for block in raw:
        if not isinstance(block, dict):
            parts.append(_TextContentPart(text=json.dumps(block)))
            continue

        t = block.get("type")
        if t == "text" and isinstance(block.get("text"), str):
            parts.append(_TextContentPart(text=cast(str, block["text"])))
        elif t == "image_url":
            iu = block.get("image_url")
            url = iu if isinstance(iu, str) else str((iu or {}).get("url", ""))
            parts.append(_ImageUrlContentPart(image_url=_ImageUrl(url=url)))

        # Any other types are not recognized by the CrowdStrike AIDR API.

    return parts

