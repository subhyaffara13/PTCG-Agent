
def _parse_exts_opts(exts_opts: memoryview) -> dict[bytes, bytes]:
    result: dict[bytes, bytes] = {}
    last_name = None
    while exts_opts:
        name, exts_opts = _get_sshstr(exts_opts)
        bname: bytes = bytes(name)
        if bname in result:
            raise ValueError("Duplicate name")
        if last_name is not None and bname < last_name:
            raise ValueError("Fields not lexically sorted")
        value, exts_opts = _get_sshstr(exts_opts)
        if len(value) > 0:
            value, extra = _get_sshstr(value)
            if len(extra) > 0:
                raise ValueError("Unexpected extra data after value")
        result[bname] = bytes(value)
        last_name = bname
    return result

