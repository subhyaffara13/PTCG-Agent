
def _smime_remove_text_headers(data: bytes) -> bytes:
    m = email.message_from_bytes(data)
    # Using get() instead of get_content_type() since it has None as default,
    # where the latter has "text/plain". Both methods are case-insensitive.
    content_type = m.get("content-type")
    if content_type is None:
        raise ValueError(
            "Decrypted MIME data has no 'Content-Type' header. "
            "Please remove the 'Text' option to parse it manually."
        )
    if "text/plain" not in content_type:
        raise ValueError(
            f"Decrypted MIME data content type is '{content_type}', not "
            "'text/plain'. Remove the 'Text' option to parse it manually."
        )
    return bytes(m.get_payload(decode=True))

