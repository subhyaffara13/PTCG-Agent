
def _dm_rref(M, *, method='auto'):
    """
    Compute the reduced row echelon form of a ``DomainMatrix``.

    This function is the implementation of :meth:`DomainMatrix.rref`.

    Chooses the best algorithm depending on the domain, shape, and sparsity of
    the matrix as well as things like the bit count in the case of :ref:`ZZ` or
    :ref:`QQ`. The result is returned over the field associated with the domain
    of the Matrix.

    See Also
    ========

    sympy.polys.matrices.domainmatrix.DomainMatrix.rref
        The ``DomainMatrix`` method that calls this function.
    sympy.polys.matrices.rref._dm_rref_den
        Alternative function for computing RREF with denominator.
    """
    method, use_fmt = _dm_rref_choose_method(M, method, denominator=False)

    M, old_fmt = _dm_to_fmt(M, use_fmt)

    if method == 'GJ':
        # Use Gauss-Jordan with division over the associated field.
        Mf = _to_field(M)
        M_rref, pivots = _dm_rref_GJ(Mf)

    elif method == 'FF':
        # Use fraction-free GJ over the current domain.
        M_rref_f, den, pivots = _dm_rref_den_FF(M)
        M_rref = _to_field(M_rref_f) / den

    elif method == 'CD':
        # Clear denominators and use fraction-free GJ in the associated ring.
        _, Mr = M.clear_denoms_rowwise(convert=True)
        M_rref_f, den, pivots = _dm_rref_den_FF(Mr)
        M_rref = _to_field(M_rref_f) / den

    else:
        raise ValueError(f"Unknown method for rref: {method}")

    M_rref, _ = _dm_to_fmt(M_rref, old_fmt)

    # Invariants:
    #   - M_rref is in the same format (sparse or dense) as the input matrix.
    #   - M_rref is in the associated field domain and any denominator was
    #     divided in (so is implicitly 1 now).

    return M_rref, pivots

