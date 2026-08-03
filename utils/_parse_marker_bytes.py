import re

def _parse_marker_bytes(data: bytes) -> _MarkerInfo | None:
    # Trust nothing about attacker-controlled markers; any deviation returns None so callers fall through
    # to stale cleanup. ``re.match`` caches compiled patterns internally, so the regex is built only once
    # despite being defined inline.
    if not data or len(data) > _MAX_MARKER_SIZE:
        return None
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError:
        return None
    match = re.match(
        r"""
        \A                                  # start of string
        (?P<token>    [0-9a-f]{32}     ) \n # 128-bit hex token
        (?P<pid>      [1-9][0-9]{0,9}  ) \n # decimal pid: no leading zero, ≤ 10 digits
        (?P<hostname> [\x21-\x7e]{1,253})   # printable non-whitespace ASCII (RFC 1123 hostname limit)
        \n*                                 # tolerate sloppy writers that append extra newlines
        \Z                                  # end of string
        """,
        text,
        re.VERBOSE,
    )
    if match is None:
        return None
    pid = int(match["pid"], 10)
    if pid > 2**31 - 1:
        return None
    return _MarkerInfo(token=match["token"], pid=pid, hostname=match["hostname"])

