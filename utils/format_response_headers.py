
def format_response_headers(
    http_version: bytes,
    status: int,
    reason_phrase: bytes | None,
    headers: list[tuple[bytes, bytes]],
) -> str:
    version = http_version.decode("ascii")
    reason = (
        codes.get_reason_phrase(status)
        if reason_phrase is None
        else reason_phrase.decode("ascii")
    )
    lines = [f"{version} {status} {reason}"] + [
        f"{name.decode('ascii')}: {value.decode('ascii')}" for name, value in headers
    ]
    return "\n".join(lines)

