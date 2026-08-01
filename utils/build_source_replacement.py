
def build_source_replacement(
    old_arg_sources: list[Source | None],
    new_arg_sources: list[Source | None],
) -> dict[Source, Source]:
    """Map old arg sources to new arg sources for remapping captured variable sources."""
    return {
        old: new
        for old, new in zip(old_arg_sources, new_arg_sources)
        if old is not None and new is not None and old != new
    }

