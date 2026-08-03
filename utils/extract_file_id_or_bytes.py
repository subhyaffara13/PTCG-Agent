from typing import Optional, Tuple

def extract_file_id_or_bytes(
    source_url: str,
    model: str,
) -> Tuple[Optional[str], Optional[bytes], Optional[str]]:
    if source_url.startswith(REDUCTO_ID_PREFIX):
        return source_url, None, None

    if source_url.startswith("http://") or source_url.startswith("https://"):
        _raise_bad_request(
            "Reducto requires type='file' (auto-uploaded) or a reducto:// id. Plain http(s) URLs are not supported; upload the file first.",
            model=model,
        )

    if not source_url.startswith("data:"):
        _raise_bad_request(
            "Reducto requires a reducto:// id or a base64 data URI after OCR preprocessing.",
            model=model,
        )

    try:
        header, encoded = source_url.split(",", 1)
    except ValueError:
        _raise_bad_request("Invalid Reducto data URI provided.", model=model)

    if ";base64" not in header:
        _raise_bad_request(
            "Reducto only supports base64-encoded data URIs.", model=model
        )

    mime = header.removeprefix("data:").split(";")[0] or "application/octet-stream"
    try:
        raw_bytes = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        _raise_bad_request("Invalid Reducto base64 payload provided.", model=model)

    return None, raw_bytes, mime

