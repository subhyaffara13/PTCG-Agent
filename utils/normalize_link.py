
def normalizeLink(url: str) -> str:
    """Normalize destination URLs in links

    ::

        [label]:   destination   'title'
                ^^^^^^^^^^^
    """
    parsed = mdurl.parse(url, slashes_denote_host=True)

    # Encode hostnames in urls like:
    # `http://host/`, `https://host/`, `mailto:user@host`, `//host/`
    #
    # We don't encode unknown schemas, because it's likely that we encode
    # something we shouldn't (e.g. `skype:name` treated as `skype:host`)
    #
    if parsed.hostname and (
        not parsed.protocol or parsed.protocol in RECODE_HOSTNAME_FOR
    ):
        with suppress(Exception):
            parsed = parsed._replace(hostname=_punycode.to_ascii(parsed.hostname))

    return mdurl.encode(mdurl.format(parsed))

