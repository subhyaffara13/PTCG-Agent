
def _codec_error_url_quote(e: UnicodeError) -> tuple[str, int]:
    """Used in :func:`uri_to_iri` after unquoting to re-quote any
    invalid bytes.
    """
    # the docs state that UnicodeError does have these attributes,
    # but mypy isn't picking them up
    out = quote(e.object[e.start : e.end], safe="")  # type: ignore
    return out, e.end  # type: ignore

