
def normalise_build_source_list(sources: list[BuildSource]) -> list[tuple[str, str | None]]:
    return sorted(
        (s.module, (normalise_path(s.base_dir) if s.base_dir is not None else None))
        for s in sources
    )

