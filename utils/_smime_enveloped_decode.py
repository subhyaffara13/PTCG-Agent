
def _smime_enveloped_decode(data: bytes) -> bytes:
    m = email.message_from_bytes(data)
    if m.get_content_type() not in {
        "application/x-pkcs7-mime",
        "application/pkcs7-mime",
    }:
        raise ValueError("Not an S/MIME enveloped message")
    return bytes(m.get_payload(decode=True))

