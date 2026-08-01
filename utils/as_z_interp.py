
def as_z_interp(z_interp: ZInterp | str) -> ZInterp:
    """Coerce a ZInterp or string value to a ZInterp.

    Args:
        z_interp (ZInterp or str): Value to convert.

    Return:
        ZInterp: Converted value.
    """
    if isinstance(z_interp, str):
        try:
            return ZInterp.__members__[z_interp]
        except KeyError as e:
            raise ValueError(f"'{z_interp}' is not a valid ZInterp") from e
    else:
        return z_interp

