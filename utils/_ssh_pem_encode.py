
def _ssh_pem_encode(
    data: utils.Buffer,
    prefix: bytes = _SK_START + b"\n",
    suffix: bytes = _SK_END + b"\n",
) -> bytes:
    return b"".join([prefix, _base64_encode(data), suffix])

