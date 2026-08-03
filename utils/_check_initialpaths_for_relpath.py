from pathlib import Path


def _check_initialpaths_for_relpath(
    initial_paths: frozenset[Path], path: Path
) -> str | None:
    if path in initial_paths:
        return ""

    for parent in path.parents:
        if parent in initial_paths:
            return str(path.relative_to(parent))

    return None

