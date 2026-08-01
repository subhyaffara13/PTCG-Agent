
def _as_version(version: Union[str, LegacyVersion, Version]
) -> Union[LegacyVersion, Version]:
    """
    Return a packaging Version-like object suitable for sorting
    """
    if isinstance(version, (LegacyVersion, Version)):
        return version
    else:
        # drop possible trailing star that make this a non version-like string
        version = version.rstrip(".*")
        return parse(version)

