import re

def split_url(url: str) -> SplitURLType:
    """Split URL into parts."""
    # Adapted from urllib.parse.urlsplit
    # Only lstrip url as some applications rely on preserving trailing space.
    # (https://url.spec.whatwg.org/#concept-basic-url-parser would strip both)
    url = url.lstrip(WHATWG_C0_CONTROL_OR_SPACE)
    for b in UNSAFE_URL_BYTES_TO_REMOVE:
        if b in url:
            url = url.replace(b, "")

    scheme = netloc = query = fragment = ""
    i = url.find(":")
    if i > 0 and url[0] in scheme_chars:
        for c in url[1:i]:
            if c not in scheme_chars:
                break
        else:
            scheme, url = url[:i].lower(), url[i + 1 :]
    has_hash = "#" in url
    has_question_mark = "?" in url
    if url[:2] == "//":
        delim = len(url)  # position of end of domain part of url, default is end
        if has_hash and has_question_mark:
            delim_chars = "/?#"
        elif has_question_mark:
            delim_chars = "/?"
        elif has_hash:
            delim_chars = "/#"
        else:
            delim_chars = "/"
        for c in delim_chars:  # look for delimiters; the order is NOT important
            wdelim = url.find(c, 2)  # find first of this delim
            if wdelim >= 0 and wdelim < delim:  # if found
                delim = wdelim  # use earliest delim position
        netloc = url[2:delim]
        url = url[delim:]
        # Backslash is not valid in the authority component per RFC 3986.
        # WHATWG parsers treat \ as a path separator for special schemes, so
        # accepting it in the authority can cause host parsing ambiguity.
        if "\\" in netloc:
            raise ValueError(
                "Invalid URL: backslash ('\\') is not allowed in the authority "
                "component per RFC 3986."
            )
        has_left_bracket = "[" in netloc
        has_right_bracket = "]" in netloc
        if (has_left_bracket and not has_right_bracket) or (
            has_right_bracket and not has_left_bracket
        ):
            raise ValueError("Invalid IPv6 URL")
        if has_left_bracket:
            # Per RFC 3986, brackets are only valid at the START of the host
            # for IP-literal addresses. Text before '[' (e.g. '127.0.0.1[::1]')
            # is invalid and must be rejected to prevent SSRF bypasses. The
            # count checks reject URLs with more than one bracket pair in the
            # host subcomponent (e.g. 'http://[:localhost[]].google:80'),
            # which would otherwise resolve to an unintended host.
            hostinfo = netloc.rpartition("@")[2]
            if hostinfo[0] != "[" or hostinfo.count("[") > 1 or hostinfo.count("]") > 1:
                raise ValueError("Invalid IPv6 URL")
            bracketed_host, _, after_bracket = hostinfo[1:].partition("]")
            # Per RFC 3986 §3.2.2, after the closing ']' of an IP-literal
            # only ":" <port> or end-of-authority is valid. Any other text
            # (e.g. '[::1]allowed.example:1') must be rejected to prevent
            # host-confusion where the suffix is silently dropped.
            if after_bracket and after_bracket[0] != ":":
                raise ValueError("Invalid IPv6 URL")
            # Valid bracketed hosts are defined in
            # https://www.rfc-editor.org/rfc/rfc3986#page-49
            # https://url.spec.whatwg.org/
            if bracketed_host and bracketed_host[0] == "v":
                if not re.match(r"\Av[a-fA-F0-9]+\..+\Z", bracketed_host):
                    raise ValueError("IPvFuture address is invalid")
            elif ":" not in bracketed_host:
                raise ValueError("The IPv6 content between brackets is not valid")
    if has_hash:
        url, _, fragment = url.partition("#")
    if has_question_mark:
        url, _, query = url.partition("?")
    if netloc and not netloc.isascii():
        _check_netloc(netloc)
    return scheme, netloc, url, query, fragment

