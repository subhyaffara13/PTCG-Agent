from typing import Optional

def resolve_driver_info(
    driver_info: Optional[DriverInfo] | object = SENTINEL,
    lib_name: Optional[str] | object = SENTINEL,
    lib_version: Optional[str] | object = SENTINEL,
) -> Optional[DriverInfo]:
    """Resolve driver_info from parameters.

    If driver_info is provided, use it. Otherwise, create DriverInfo from
    lib_name and lib_version (using defaults only for sentinel values).

    Parameters
    ----------
    driver_info : DriverInfo, optional
        The DriverInfo instance to use
    lib_name : str, optional
        The library name (default: "redis-py")
    lib_version : str, optional
        The library version (default: auto-detected)

    Returns
    -------
    DriverInfo, optional
        The resolved DriverInfo instance
    """
    if driver_info is SENTINEL:
        if lib_name is None and lib_version is None:
            return None
        return DriverInfo(name=lib_name, lib_version=lib_version)

    if driver_info is None or isinstance(driver_info, DriverInfo):
        return driver_info

    raise TypeError("driver_info must be a DriverInfo instance or None")

