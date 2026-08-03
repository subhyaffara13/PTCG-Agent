import sys

def safe_print(text: str) -> None:
    """Print a text replacing chars not representable in stdout encoding."""
    # If `sys.stdout` encoding is not the same as out (usually UTF8) string,
    # if may cause painful crashes. I don't want to reconfigure `sys.stdout`
    # to do `errors = "replace"` as that sounds scary.
    out_encoding = sys.stdout.encoding
    if out_encoding is not None:
        # Can be None if stdout is replaced (including our own tests). This should be
        # safe to omit if the actual stream doesn't care about encoding.
        text = text.encode(out_encoding, errors="replace").decode(out_encoding, errors="replace")
    print(text)

