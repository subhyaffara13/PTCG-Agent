
def parse_mimetype(mimetype: str) -> MimeType:
    """Parses a MIME type into its components.

    mimetype is a MIME type string.

    Returns a MimeType object.

    Example:

    >>> parse_mimetype('text/html; charset=utf-8')
    MimeType(type='text', subtype='html', suffix='',
             parameters={'charset': 'utf-8'})

    """
    if not mimetype:
        return MimeType(
            type="", subtype="", suffix="", parameters=MultiDictProxy(MultiDict())
        )

    parts = mimetype.split(";")
    params: MultiDict[str] = MultiDict()
    for item in parts[1:]:
        if not item:
            continue
        key, _, value = item.partition("=")
        params.add(key.lower().strip(), value.strip(' "'))

    fulltype = parts[0].strip().lower()
    if fulltype == "*":
        fulltype = "*/*"

    mtype, _, stype = fulltype.partition("/")
    stype, _, suffix = stype.partition("+")

    return MimeType(
        type=mtype, subtype=stype, suffix=suffix, parameters=MultiDictProxy(params)
    )

