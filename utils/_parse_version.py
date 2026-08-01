
def _parse_version(version: str) -> tuple[int, int, int]:
    """Parse a version string into a tuple of 3 integers.

    Args:
        version: A version string.

    Raises:
        ValueError: If the version string is invalid.

    Returns:
        A tuple of 3 integers.
    """
    version_integers: tuple[int, ...]
    try:
        version_integers = tuple(
            map(int, version.split(".")),
        )
    except ValueError:
        raise ValueError(
            f"unicode version string {version!r} is badly formatted"
        ) from None
    while len(version_integers) < 3:
        version_integers = version_integers + (0,)
    triple = cast("tuple[int, int, int]", version_integers[:3])
    return triple


def _parse_version(v: str) -> tuple[int, ...]:
    """Parse a version string like '4.1.0' into a tuple of ints."""
    return tuple(int(x) for x in v.split(".")[:3])

