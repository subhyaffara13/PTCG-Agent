
def escape_golang_path(path: str) -> str:
    """
    Return an case-encoded module path or version name.

    This is done by replacing every uppercase letter with an exclamation mark followed by the
    corresponding lower-case letter, in order to avoid ambiguity when serving from case-insensitive
    file systems.

    See https://golang.org/ref/mod#goproxy-protocol.
    """
    escaped_path = ""
    for c in path:
        if c >= "A" and c <= "Z":
            # replace uppercase with !lowercase
            escaped_path += "!" + chr(ord(c) + ord("a") - ord("A"))
        else:
            escaped_path += c
    return escaped_path

