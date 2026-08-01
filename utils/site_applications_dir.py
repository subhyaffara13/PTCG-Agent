
def site_applications_dir(
    multipath: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
) -> str:
    """:param multipath: See `multipath <platformdirs.api.PlatformDirsABC.multipath>`.
    :param ensure_exists: See `ensure_exists <platformdirs.api.PlatformDirsABC.ensure_exists>`.

    :returns: applications directory shared by users

    """
    return PlatformDirs(
        multipath=multipath,
        ensure_exists=ensure_exists,
    ).site_applications_dir

