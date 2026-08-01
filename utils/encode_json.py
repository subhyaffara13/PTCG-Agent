
def encode_json(json: Any) -> tuple[dict[str, str], ByteStream]:
    body = json_dumps(
        json, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    content_length = str(len(body))
    content_type = "application/json"
    headers = {"Content-Length": content_length, "Content-Type": content_type}
    return headers, ByteStream(body)

