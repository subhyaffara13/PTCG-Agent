from pathlib import Path


def _pretty_fixture_path(invocation_dir: Path, func) -> str:
    loc = Path(getlocation(func, invocation_dir))
    prefix = Path("...", "_pytest")
    try:
        return str(prefix / loc.relative_to(_PYTEST_DIR))
    except ValueError:
        return bestrelpath(invocation_dir, loc)

