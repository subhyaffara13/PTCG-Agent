
def select_from_pylock_path_or_url(
    pylock_path_or_url: str,
    session: PipSession,
) -> Iterator[
    tuple[
        Package,
        PackageVcs | PackageDirectory | PackageArchive | PackageWheel | PackageSdist,
    ]
]:
    try:
        pylock_content = _get_pylock_path_or_url_content(pylock_path_or_url, session)
    except Exception as exc:
        raise InstallationError(
            f"Error reading pylock file {pylock_path_or_url!r}: {exc}"
        ) from exc

    try:
        lock = Pylock.from_dict(tomllib.loads(pylock_content))
    except Exception as exc:
        raise InstallationError(
            f"Invalid pylock file {pylock_path_or_url!r}: {exc}"
        ) from exc

    try:
        yield from lock.select()
    except Exception as exc:
        raise InstallationError(
            f"Cannot select requirements from pylock file {pylock_path_or_url!r}: {exc}"
        ) from exc

