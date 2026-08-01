
def parse_content_disposition(
    header: str | None,
) -> tuple[str | None, dict[str, str]]:
    def is_token(string: str) -> bool:
        return bool(string) and TOKEN >= set(string)

    def is_quoted(string: str) -> bool:
        return string[0] == string[-1] == '"'

    def is_rfc5987(string: str) -> bool:
        return is_token(string) and string.count("'") == 2

    def is_extended_param(string: str) -> bool:
        return string.endswith("*")

    def is_continuous_param(string: str) -> bool:
        pos = string.find("*") + 1
        if not pos:
            return False
        substring = string[pos:-1] if string.endswith("*") else string[pos:]
        return substring.isdigit()

    def unescape(text: str, *, chars: str = "".join(map(re.escape, CHAR))) -> str:
        return re.sub(f"\\\\([{chars}])", "\\1", text)

    if not header:
        return None, {}

    disptype, *parts = header.split(";")
    if not is_token(disptype):
        warnings.warn(BadContentDispositionHeader(header))
        return None, {}

    params: dict[str, str] = {}
    while parts:
        item = parts.pop(0)

        if not item:  # To handle trailing semicolons
            warnings.warn(BadContentDispositionHeader(header))
            continue

        if "=" not in item:
            warnings.warn(BadContentDispositionHeader(header))
            return None, {}

        key, value = item.split("=", 1)
        key = key.lower().strip()
        value = value.lstrip()

        if key in params:
            warnings.warn(BadContentDispositionHeader(header))
            return None, {}

        if not is_token(key):
            warnings.warn(BadContentDispositionParam(item))
            continue

        elif is_continuous_param(key):
            if is_quoted(value):
                value = unescape(value[1:-1])
            elif not is_token(value):
                warnings.warn(BadContentDispositionParam(item))
                continue

        elif is_extended_param(key):
            if is_rfc5987(value):
                encoding, _, value = value.split("'", 2)
                encoding = encoding or "utf-8"
            else:
                warnings.warn(BadContentDispositionParam(item))
                continue

            try:
                value = unquote(value, encoding, "strict")
            except UnicodeDecodeError:  # pragma: nocover
                warnings.warn(BadContentDispositionParam(item))
                continue

        else:
            failed = True
            if is_quoted(value):
                failed = False
                value = unescape(value[1:-1].lstrip("\\/"))
            elif is_token(value):
                failed = False
            elif parts:
                # maybe just ; in filename, in any case this is just
                # one case fix, for proper fix we need to redesign parser
                _value = f"{value};{parts[0]}"
                if is_quoted(_value):
                    parts.pop(0)
                    value = unescape(_value[1:-1].lstrip("\\/"))
                    failed = False

            if failed:
                warnings.warn(BadContentDispositionHeader(header))
                return None, {}

        params[key] = value

    return disptype.lower(), params


def parse_content_disposition(content_disposition: str, default_filename: str) -> str:
    """
    Parse the "filename" value from a Content-Disposition header, and
    return the default filename if the result is empty.
    """
    m = email.message.Message()
    m["content-type"] = content_disposition
    filename = m.get_param("filename")
    if filename:
        # We need to sanitize the filename to prevent directory traversal
        # in case the filename contains ".." path parts.
        filename = sanitize_content_filename(str(filename))
    return filename or default_filename

