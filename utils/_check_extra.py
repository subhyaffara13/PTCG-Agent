
def _check_extra(extra, reqs):
    _name, _sep, marker = extra.partition(':')
    try:
        _check_marker(marker)
    except InvalidMarker:
        msg = f"Invalid environment marker: {marker} ({extra!r})"
        raise DistutilsSetupError(msg) from None
    list(_reqs.parse(reqs))

