
def from_Decimal(x, prec=None, rnd=round_fast):
    """Create a raw mpf from a Decimal, rounding if necessary.
    If prec is not specified, use the equivalent bit precision
    of the number of significant digits in x."""
    if x.is_nan(): return fnan
    if x.is_infinite(): return fninf if x.is_signed() else finf
    if prec is None:
        prec = int(len(x.as_tuple()[1])*3.3219280948873626)
    return from_str(str(x), prec, rnd)

