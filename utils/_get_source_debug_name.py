
def _get_source_debug_name(source: Source | None) -> str:
    if source is None:
        return "<unknown source>"
    else:
        try:
            return source.name
        except NotImplementedError:
            return "<unknown source>"

