
def build_signature_string(
    method: str, path: str, headers: dict, signed_headers: list
) -> str:
    lines = []
    for header in signed_headers:
        if header == "(request-target)":
            value = f"{method.lower()} {path}"
        else:
            value = headers[header]
        lines.append(f"{header}: {value}")
    return "\n".join(lines)

