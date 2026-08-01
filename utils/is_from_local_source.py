
def is_from_local_source(source: Source, *, only_allow_input: bool = False) -> bool:
    return get_local_source_name(source, only_allow_input=only_allow_input) is not None

