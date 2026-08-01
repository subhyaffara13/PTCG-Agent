
def get_local_source_name(
    source: Source, *, only_allow_input: bool = False
) -> str | None:
    if isinstance(source, ChainedSource):
        return get_local_source_name(source.base, only_allow_input=only_allow_input)
    if not isinstance(source, LocalSource):
        return None
    if only_allow_input and not source.is_input:
        return None
    return source.local_name

