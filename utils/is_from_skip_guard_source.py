
def is_from_skip_guard_source(source: Source) -> bool:
    if isinstance(source, SkipGuardSource):
        return True

    if isinstance(source, ChainedSource):
        return is_from_skip_guard_source(source.base)

    return False

