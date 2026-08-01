
def to_col(coeffs):
    r"""Transform a list of integer coefficients into a column vector."""
    return DomainMatrix([[ZZ(c) for c in coeffs]], (1, len(coeffs)), ZZ).transpose()

