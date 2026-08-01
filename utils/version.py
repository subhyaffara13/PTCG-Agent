
def version(pretty: bool = False, best: bool = False) -> str:
    """
    Return the version of the current OS distribution, as a human-readable
    string.

    If *pretty* is false, the version is returned without codename (e.g.
    "7.0").

    If *pretty* is true, the codename in parenthesis is appended, if the
    codename is non-empty (e.g. "7.0 (Maipo)").

    Some distributions provide version numbers with different precisions in
    the different sources of distribution information. Examining the different
    sources in a fixed priority order does not always yield the most precise
    version (e.g. for Debian 8.2, or CentOS 7.1).

    Some other distributions may not provide this kind of information. In these
    cases, an empty string would be returned. This behavior can be observed
    with rolling releases distributions (e.g. Arch Linux).

    The *best* parameter can be used to control the approach for the returned
    version:

    If *best* is false, the first non-empty version number in priority order of
    the examined sources is returned.

    If *best* is true, the most precise version number out of all examined
    sources is returned.

    **Lookup hierarchy:**

    In all cases, the version number is obtained from the following sources.
    If *best* is false, this order represents the priority order:

    * the value of the "VERSION_ID" attribute of the os-release file,
    * the value of the "Release" attribute returned by the lsb_release
      command,
    * the version number parsed from the "<version_id>" field of the first line
      of the distro release file,
    * the version number parsed from the "PRETTY_NAME" attribute of the
      os-release file, if it follows the format of the distro release files.
    * the version number parsed from the "Description" attribute returned by
      the lsb_release command, if it follows the format of the distro release
      files.
    """
    return _distro.version(pretty, best)


def version(distribution_name: str) -> str:
    """Get the version string for the named package.

    :param distribution_name: The name of the distribution package to query.
    :return: The version string for the package as defined in the package's
        "Version" metadata key.
    """
    return distribution(distribution_name).version


def version(feature: str) -> str | None:
    """
    :param feature:
        The module, codec, or feature to check for.
    :returns:
        The version number as a string, or ``None`` if unknown or not available.
    """
    if feature in modules:
        return version_module(feature)
    if feature in codecs:
        return version_codec(feature)
    if feature in features:
        return version_feature(feature)
    return None


def version() -> str:
    result = call("--version")

    # result is of the form:
    # pip <version> from <directory> (python <python version>)

    return result.split(" ")[1]


def version() -> None:
    """Print CLI version."""
    print(__version__)


def version():
    """
    Returns the version of the NCCL.


    This function returns a tuple containing the major, minor, and patch version numbers of the NCCL.
    The suffix is also included in the tuple if a version suffix exists.
    Returns:
        tuple: The version information of the NCCL.
    """
    ver = torch._C._nccl_version()
    major = ver >> 32
    minor = (ver >> 16) & 65535
    patch = ver & 65535
    suffix = torch._C._nccl_version_suffix().decode("utf-8")
    if suffix == "":
        return (major, minor, patch)
    else:
        return (major, minor, patch, suffix)


def version():
    """Return the version of cuDNN."""
    if not _init():
        return None
    return __cudnn_version


def version() -> int | None:
    """Return the version of cuSPARSELt"""
    if not _init():
        return None
    return __cusparselt_version


def version(value: Callable | Iterable[str | int] | str) -> str:
    """When getting the version directly from an attribute,
    it should be normalised to string.
    """
    _value = value() if callable(value) else value

    if isinstance(_value, str):
        return _value
    if hasattr(_value, '__iter__'):
        return '.'.join(map(str, _value))
    return f'{_value}'


def version(distribution_name: str) -> str:
    """Get the version string for the named package.

    :param distribution_name: The name of the distribution package to query.
    :return: The version string for the package as defined in the package's
        "Version" metadata key.
    """
    return distribution(distribution_name).version


def version(pretty: bool = False, best: bool = False) -> str:
    """
    Return the version of the current OS distribution, as a human-readable
    string.

    If *pretty* is false, the version is returned without codename (e.g.
    "7.0").

    If *pretty* is true, the codename in parenthesis is appended, if the
    codename is non-empty (e.g. "7.0 (Maipo)").

    Some distributions provide version numbers with different precisions in
    the different sources of distribution information. Examining the different
    sources in a fixed priority order does not always yield the most precise
    version (e.g. for Debian 8.2, or CentOS 7.1).

    Some other distributions may not provide this kind of information. In these
    cases, an empty string would be returned. This behavior can be observed
    with rolling releases distributions (e.g. Arch Linux).

    The *best* parameter can be used to control the approach for the returned
    version:

    If *best* is false, the first non-empty version number in priority order of
    the examined sources is returned.

    If *best* is true, the most precise version number out of all examined
    sources is returned.

    **Lookup hierarchy:**

    In all cases, the version number is obtained from the following sources.
    If *best* is false, this order represents the priority order:

    * the value of the "VERSION_ID" attribute of the os-release file,
    * the value of the "Release" attribute returned by the lsb_release
      command,
    * the version number parsed from the "<version_id>" field of the first line
      of the distro release file,
    * the version number parsed from the "PRETTY_NAME" attribute of the
      os-release file, if it follows the format of the distro release files.
    * the version number parsed from the "Description" attribute returned by
      the lsb_release command, if it follows the format of the distro release
      files.
    """
    return _distro.version(pretty, best)


def version(ctx: click.Context):
    """Show the LiteLLM Proxy CLI and server version."""
    print_version(ctx.obj.get("base_url"), ctx.obj.get("api_key"))


def version() -> None:
    """Print information about the hf version."""
    out.result("hf version", version=__version__)

