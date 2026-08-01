
def normalizeLinkText(url: str) -> str:
    """Normalize autolink content

    ::

        <destination>
         ~~~~~~~~~~~
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
            parsed = parsed._replace(hostname=_punycode.to_unicode(parsed.hostname))

    # add '%' to exclude list because of https://github.com/markdown-it/markdown-it/issues/720
    return mdurl.decode(mdurl.format(parsed), mdurl.DECODE_DEFAULT_CHARS + "%")

