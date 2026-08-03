from pathlib import Path


def site_state_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
) -> Path:
    """:param appname: See `appname <platformdirs.api.PlatformDirsABC.appname>`.
    :param appauthor: See `appauthor <platformdirs.api.PlatformDirsABC.appauthor>`.
    :param version: See `version <platformdirs.api.PlatformDirsABC.version>`.
    :param ensure_exists: See `ensure_exists <platformdirs.api.PlatformDirsABC.ensure_exists>`.

    :returns: state path shared by users

    """
    return PlatformDirs(
        appname=appname,
        appauthor=appauthor,
        version=version,
        ensure_exists=ensure_exists,
    ).site_state_path

