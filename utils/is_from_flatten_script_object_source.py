
def is_from_flatten_script_object_source(source: Source) -> bool:
    if isinstance(source, FlattenScriptObjectSource):
        return True
    elif isinstance(source, ChainedSource):
        return is_from_flatten_script_object_source(source.base)
    return False

