
def _safe_header(string: str) -> str:
    if _FORBIDDEN_HEADER_CHARS_RE.search(string) is not None:
        raise ValueError(
            "Forbidden control character detected in headers. "
            "Potential header injection attack."
        )
    return string

