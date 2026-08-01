
def _real_dtype_for_complex(dtyp, *, xp):
    if xp.isdtype(dtyp, 'real floating'):
        return dtyp
    if dtyp == xp.complex64:
        return xp.float32
    elif dtyp == xp.complex128:
        return xp.float64
    else:
        raise ValueError(f"Unknown dtype {dtyp}.")

