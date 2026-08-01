
def urlparse(url: str = "", **kwargs: str | None) -> ParseResult:
    # Initial basic checks on allowable URLs.
    # ---------------------------------------

    # Hard limit the maximum allowable URL length.
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL("URL too long")

    # If a URL includes any ASCII control characters including \t, \r, \n,
    # then treat it as invalid.
    if any(char.isascii() and not char.isprintable() for char in url):
        char = next(char for char in url if char.isascii() and not char.isprintable())
        idx = url.find(char)
        error = (
            f"Invalid non-printable ASCII character in URL, {char!r} at position {idx}."
        )
        raise InvalidURL(error)

    # Some keyword arguments require special handling.
    # ------------------------------------------------

    # Coerce "port" to a string, if it is provided as an integer.
    if "port" in kwargs:
        port = kwargs["port"]
        kwargs["port"] = str(port) if isinstance(port, int) else port

    # Replace "netloc" with "host and "port".
    if "netloc" in kwargs:
        netloc = kwargs.pop("netloc") or ""
        kwargs["host"], _, kwargs["port"] = netloc.partition(":")

    # Replace "username" and/or "password" with "userinfo".
    if "username" in kwargs or "password" in kwargs:
        username = quote(kwargs.pop("username", "") or "", safe=USERNAME_SAFE)
        password = quote(kwargs.pop("password", "") or "", safe=PASSWORD_SAFE)
        kwargs["userinfo"] = f"{username}:{password}" if password else username

    # Replace "raw_path" with "path" and "query".
    if "raw_path" in kwargs:
        raw_path = kwargs.pop("raw_path") or ""
        kwargs["path"], seperator, kwargs["query"] = raw_path.partition("?")
        if not seperator:
            kwargs["query"] = None

    # Ensure that IPv6 "host" addresses are always escaped with "[...]".
    if "host" in kwargs:
        host = kwargs.get("host") or ""
        if ":" in host and not (host.startswith("[") and host.endswith("]")):
            kwargs["host"] = f"[{host}]"

    # If any keyword arguments are provided, ensure they are valid.
    # -------------------------------------------------------------

    for key, value in kwargs.items():
        if value is not None:
            if len(value) > MAX_URL_LENGTH:
                raise InvalidURL(f"URL component '{key}' too long")

            # If a component includes any ASCII control characters including \t, \r, \n,
            # then treat it as invalid.
            if any(char.isascii() and not char.isprintable() for char in value):
                char = next(
                    char for char in value if char.isascii() and not char.isprintable()
                )
                idx = value.find(char)
                error = (
                    f"Invalid non-printable ASCII character in URL {key} component, "
                    f"{char!r} at position {idx}."
                )
                raise InvalidURL(error)

            # Ensure that keyword arguments match as a valid regex.
            if not COMPONENT_REGEX[key].fullmatch(value):
                raise InvalidURL(f"Invalid URL component '{key}'")

    # The URL_REGEX will always match, but may have empty components.
    url_match = URL_REGEX.match(url)
    assert url_match is not None
    url_dict = url_match.groupdict()

    # * 'scheme', 'authority', and 'path' may be empty strings.
    # * 'query' may be 'None', indicating no trailing "?" portion.
    #   Any string including the empty string, indicates a trailing "?".
    # * 'fragment' may be 'None', indicating no trailing "#" portion.
    #   Any string including the empty string, indicates a trailing "#".
    scheme = kwargs.get("scheme", url_dict["scheme"]) or ""
    authority = kwargs.get("authority", url_dict["authority"]) or ""
    path = kwargs.get("path", url_dict["path"]) or ""
    query = kwargs.get("query", url_dict["query"])
    frag = kwargs.get("fragment", url_dict["fragment"])

    # The AUTHORITY_REGEX will always match, but may have empty components.
    authority_match = AUTHORITY_REGEX.match(authority)
    assert authority_match is not None
    authority_dict = authority_match.groupdict()

    # * 'userinfo' and 'host' may be empty strings.
    # * 'port' may be 'None'.
    userinfo = kwargs.get("userinfo", authority_dict["userinfo"]) or ""
    host = kwargs.get("host", authority_dict["host"]) or ""
    port = kwargs.get("port", authority_dict["port"])

    # Normalize and validate each component.
    # We end up with a parsed representation of the URL,
    # with components that are plain ASCII bytestrings.
    parsed_scheme: str = scheme.lower()
    parsed_userinfo: str = quote(userinfo, safe=USERINFO_SAFE)
    parsed_host: str = encode_host(host)
    parsed_port: int | None = normalize_port(port, scheme)

    has_scheme = parsed_scheme != ""
    has_authority = (
        parsed_userinfo != "" or parsed_host != "" or parsed_port is not None
    )
    validate_path(path, has_scheme=has_scheme, has_authority=has_authority)
    if has_scheme or has_authority:
        path = normalize_path(path)

    parsed_path: str = quote(path, safe=PATH_SAFE)
    parsed_query: str | None = None if query is None else quote(query, safe=QUERY_SAFE)
    parsed_frag: str | None = None if frag is None else quote(frag, safe=FRAG_SAFE)

    # The parsed ASCII bytestrings are our canonical form.
    # All properties of the URL are derived from these.
    return ParseResult(
        parsed_scheme,
        parsed_userinfo,
        parsed_host,
        parsed_port,
        parsed_path,
        parsed_query,
        parsed_frag,
    )


def urlparse(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    splitresult = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = splitresult
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    result = ParseResult(scheme, netloc, url, params, query, fragment)
    return _coerce_result(result)

