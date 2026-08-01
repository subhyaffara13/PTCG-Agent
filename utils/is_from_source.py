
def is_from_source(source: Source, target: Source) -> bool:
    if source == target:
        return True
    if isinstance(source, ChainedSource):
        return is_from_source(source.base, target)
    return False

