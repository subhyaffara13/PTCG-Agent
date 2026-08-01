
def content_disposition_header(
    disptype: str, quote_fields: bool = True, _charset: str = "utf-8", **params: str
) -> str:
    """Sets ``Content-Disposition`` header for MIME.

    This is the MIME payload Content-Disposition header from RFC 2183
    and RFC 7579 section 4.2, not the HTTP Content-Disposition from
    RFC 6266.

    disptype is a disposition type: inline, attachment, form-data.
    Should be valid extension token (see RFC 2183)

    quote_fields performs value quoting to 7-bit MIME headers
    according to RFC 7578. Set to quote_fields to False if recipient
    can take 8-bit file names and field values.

    _charset specifies the charset to use when quote_fields is True.

    params is a dict with disposition params.
    """
    if not disptype or not (TOKEN > set(disptype)):
        raise ValueError(f"bad content disposition type {disptype!r}")

    value = disptype
    if params:
        lparams = []
        for key, val in params.items():
            if not key or not (TOKEN > set(key)):
                raise ValueError(f"bad content disposition parameter {key!r}={val!r}")
            if quote_fields:
                if key.lower() == "filename":
                    qval = quote(val, "", encoding=_charset)
                    lparams.append((key, '"%s"' % qval))
                else:
                    try:
                        qval = quoted_string(val)
                    except ValueError:
                        qval = "".join(
                            (_charset, "''", quote(val, "", encoding=_charset))
                        )
                        lparams.append((key + "*", qval))
                    else:
                        lparams.append((key, '"%s"' % qval))
            else:
                qval = val.replace("\\", "\\\\").replace('"', '\\"')
                lparams.append((key, '"%s"' % qval))
        sparams = "; ".join("=".join(pair) for pair in lparams)
        value = "; ".join((value, sparams))
    return value

