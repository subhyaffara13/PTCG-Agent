
def openapi_dumps(obj: Any) -> bytes:
    """
    Serialize an object to UTF-8 encoded JSON bytes.

    Extends the standard json.dumps with support for additional types
    commonly used in the SDK, such as `datetime`, `pydantic.BaseModel`, etc.
    """
    return json.dumps(
        obj,
        cls=_CustomEncoder,
        # Uses the same defaults as httpx's JSON serialization
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode()

