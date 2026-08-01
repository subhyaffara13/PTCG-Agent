
def encode_url_path_segments(value: Any, *, field_name: str = "path") -> str:
    """Percent-encode a user-controlled URL path made of multiple segments.

    Empty segments are rejected, so leading, trailing, or consecutive slashes
    fail closed instead of being normalized by the HTTP client.
    """
    if value is None:
        raise ValueError(f"{field_name} is required")

    value_str = str(value)
    if value_str == "":
        raise ValueError(f"{field_name} is required")

    encoded_segments = []
    for segment in value_str.split("/"):
        encoded_segments.append(encode_url_path_segment(segment, field_name=field_name))

    return "/".join(encoded_segments)

