
def _get_version():
    """Return the version string used for __version__."""
    # Only shell out to a git subprocess if really needed, i.e. when we are in
    # a matplotlib git repo but not in a shallow clone, such as those used by
    # CI, as the latter would trigger a warning from setuptools_scm.
    root = Path(__file__).resolve().parents[2]
    if ((root / ".matplotlib-repo").exists()
            and (root / ".git").exists()
            and not (root / ".git/shallow").exists()):
        try:
            import setuptools_scm
        except ImportError:
            pass
        else:
            return setuptools_scm.get_version(
                root=root,
                dist_name="matplotlib",
                version_scheme="release-branch-semver",
                local_scheme="node-and-date",
                fallback_version=_version.version,
            )
    # Get the version from the _version.py file if not in repo or setuptools_scm is
    # unavailable.
    return _version.version


def _get_version(accept_header: List[str]) -> str:
    """Return the version tag from the Accept header.

    If no version is specified, returns empty string."""

    for tok in accept_header:
        if '=' not in tok:
            continue
        key, value = tok.strip().split('=', 1)
        if key == 'version':
            return value
    return ""


def _get_version():
    """
    Retrieve and format package version along with python version & OS used
    """
    return ('%s Python %s on %s' %
            (__version__, platform.python_version(), platform.system()))


def _get_version(package_name: str) -> str:
    return _package_versions.get(package_name, "N/A")

