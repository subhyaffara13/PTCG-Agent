
def check_compatibility(
    urllib3_version: str,
    chardet_version: str | None,
    charset_normalizer_version: str | None,
) -> None:
    urllib3_version_list = urllib3_version.split(".")[:3]
    assert urllib3_version_list != ["dev"]  # Verify urllib3 isn't installed from git.

    # Sometimes, urllib3 only reports its version as 16.1.
    if len(urllib3_version_list) == 2:
        urllib3_version_list.append("0")

    # Check urllib3 for compatibility.
    major, minor, patch = urllib3_version_list  # noqa: F811
    major, minor, patch = int(major), int(minor), int(patch)
    # urllib3 >= 1.21.1
    assert major >= 1
    if major == 1:
        assert minor >= 21

    # Check charset_normalizer for compatibility.
    if chardet_version:
        major, minor, patch = chardet_version.split(".")[:3]
        major, minor, patch = int(major), int(minor), int(patch)
        # chardet_version >= 3.0.2, < 8.0.0
        assert (3, 0, 2) <= (major, minor, patch) < (8, 0, 0)
    elif charset_normalizer_version:
        major, minor, patch = charset_normalizer_version.split(".")[:3]
        major, minor, patch = int(major), int(minor), int(patch)
        # charset_normalizer >= 2.0.0 < 4.0.0
        assert (2, 0, 0) <= (major, minor, patch) < (4, 0, 0)
    else:
        warnings.warn(
            "Unable to find acceptable character detection dependency "
            "(chardet or charset_normalizer).",
            RequestsDependencyWarning,
        )


def check_compatibility(urllib3_version, chardet_version, charset_normalizer_version):
    urllib3_version = urllib3_version.split(".")
    assert urllib3_version != ["dev"]  # Verify urllib3 isn't installed from git.

    # Sometimes, urllib3 only reports its version as 16.1.
    if len(urllib3_version) == 2:
        urllib3_version.append("0")

    # Check urllib3 for compatibility.
    major, minor, patch = urllib3_version  # noqa: F811
    major, minor, patch = int(major), int(minor), int(patch)
    # urllib3 >= 1.21.1
    assert major >= 1
    if major == 1:
        assert minor >= 21

    # Check charset_normalizer for compatibility.
    if chardet_version:
        major, minor, patch = chardet_version.split(".")[:3]
        major, minor, patch = int(major), int(minor), int(patch)
        # chardet_version >= 3.0.2, < 8.0.0
        assert (3, 0, 2) <= (major, minor, patch) < (8, 0, 0)
    elif charset_normalizer_version:
        major, minor, patch = charset_normalizer_version.split(".")[:3]
        major, minor, patch = int(major), int(minor), int(patch)
        # charset_normalizer >= 2.0.0 < 4.0.0
        assert (2, 0, 0) <= (major, minor, patch) < (4, 0, 0)
    else:
        # pip does not need or use character detection
        pass


def check_compatibility(version: tuple[int, ...], name: str) -> None:
    """Raises errors or warns if called with an incompatible Wheel-Version.

    pip should refuse to install a Wheel-Version that's a major series
    ahead of what it's compatible with (e.g 2.0 > 1.1); and warn when
    installing a version only minor version ahead (e.g 1.2 > 1.1).

    version: a 2-tuple representing a Wheel-Version (Major, Minor)
    name: name of wheel or package to raise exception about

    :raises UnsupportedWheel: when an incompatible Wheel-Version is given
    """
    if version[0] > VERSION_COMPATIBLE[0]:
        raise UnsupportedWheel(
            "{}'s Wheel-Version ({}) is not compatible with this version "
            "of pip".format(name, ".".join(map(str, version)))
        )
    elif version > VERSION_COMPATIBLE:
        logger.warning(
            "Installing from a newer Wheel-Version (%s)",
            ".".join(map(str, version)),
        )

