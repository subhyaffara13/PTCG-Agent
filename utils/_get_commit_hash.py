
def _get_commit_hash() -> str | None:
    """
    Use vendored versioneer code to get git hash, which handles
    git worktree correctly.
    """
    try:
        from pandas._version_meson import (  # pyright: ignore [reportMissingImports]
            __git_version__,
        )

        return __git_version__
    except ImportError:
        from pandas._version import get_versions

        versions = get_versions()
        return versions["full-revisionid"]

