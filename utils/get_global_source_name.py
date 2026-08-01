
def get_global_source_name(source: Source | None) -> str | None:
    if isinstance(source, ChainedSource):
        return get_global_source_name(source.base)
    if not isinstance(source, GlobalSource):
        return None
    return source.global_name

