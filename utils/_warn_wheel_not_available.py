
def _warn_wheel_not_available(dist):
    try:
        metadata.distribution('wheel')
    except metadata.PackageNotFoundError:
        dist.announce('WARNING: The wheel package is not available.', log.WARN)

