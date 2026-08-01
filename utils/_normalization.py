
def _normalization(norm, forward):
    """Returns the pyduccfft normalization mode from the norm argument"""
    try:
        inorm = _NORM_MAP[norm]
        return inorm if forward else (2 - inorm)
    except KeyError:
        raise ValueError(
            f'Invalid norm value {norm!r}, should '
            'be "backward", "ortho" or "forward"') from None

