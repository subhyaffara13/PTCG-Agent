
def add_all_sources_to_changed(sources: list[BuildSource], changed: list[tuple[str, str]]) -> None:
    """Add all (explicit) sources to the list changed files in place.

    Use this when re-processing of unchanged files is needed (e.g. for
    the purpose of exporting types for inspections).
    """
    changed_set = set(changed)
    changed.extend(
        [
            (bs.module, bs.path)
            for bs in sources
            if bs.path and (bs.module, bs.path) not in changed_set
        ]
    )

