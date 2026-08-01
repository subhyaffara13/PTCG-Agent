
def _convert_one(domain: str, mode: str, uts46: bool) -> bool:
    """Convert ``domain`` and write the result; return ``False`` on failure."""
    try:
        if mode == "decode":
            print(decode(domain, uts46=uts46))
        else:
            print(encode(domain, uts46=uts46).decode("ascii"))
    except IDNAError as err:
        print(f"idna: {mode} failed for {domain!r}: {err}", file=sys.stderr)
        return False
    return True

