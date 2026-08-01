
def _idna_encode(host: str) -> str:
    try:
        return idna.encode(host, uts46=True).decode("ascii")
    except UnicodeError:
        return host.encode("idna").decode("ascii")


def _idna_encode(name: str) -> bytes:
    if not name.isascii():
        try:
            import idna
        except ImportError:
            raise LocationParseError(
                "Unable to parse URL without the 'idna' module"
            ) from None

        try:
            return idna.encode(name.lower(), strict=True, std3_rules=True)
        except idna.IDNAError:
            raise LocationParseError(
                f"Name '{name}' is not a valid IDNA label"
            ) from None

    return name.lower().encode("ascii")


def _idna_encode(name: str) -> bytes:
    if not name.isascii():
        try:
            from pip._vendor import idna
        except ImportError:
            raise LocationParseError(
                "Unable to parse URL without the 'idna' module"
            ) from None

        try:
            return idna.encode(name.lower(), strict=True, std3_rules=True)
        except idna.IDNAError:
            raise LocationParseError(
                f"Name '{name}' is not a valid IDNA label"
            ) from None

    return name.lower().encode("ascii")

