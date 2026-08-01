
def fetch_build_egg(dist, req) -> metadata.Distribution | metadata.PathDistribution:
    """Fetch an egg needed for building.

    Use pip/wheel to fetch/build a wheel."""
    _DeprecatedInstaller.emit()
    _warn_wheel_not_available(dist)
    return _fetch_build_egg_no_warn(dist, req)

