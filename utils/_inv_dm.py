
def _inv_DM(dM, cancel=True):
    """Calculates the inverse using ``DomainMatrix``.

    See Also
    ========

    inv
    inverse_ADJ
    inverse_GE
    inverse_CH
    inverse_LDL
    sympy.polys.matrices.domainmatrix.DomainMatrix.inv
    """
    m, n = dM.shape
    dom = dM.domain

    if m != n:
        raise NonSquareMatrixError("A Matrix must be square to invert.")

    # Convert RR[a,b,...] to QQ[a,b,...]
    use_exact = _use_exact_domain(dom)

    if use_exact:
        dom_exact = dom.get_exact()
        dM = dM.convert_to(dom_exact)

    try:
        dMi, den = dM.inv_den()
    except DMNonInvertibleMatrixError:
        raise NonInvertibleMatrixError("Matrix det == 0; not invertible.")

    if use_exact:
        dMi = dMi.convert_to(dom)
        den = dom.convert_from(den, dom_exact)

    if cancel:
        # Convert to field and cancel with the denominator.
        if not dMi.domain.is_Field:
            dMi = dMi.to_field()
        Mi = (dMi / den).to_Matrix()
    else:
        # Convert to Matrix and divide without cancelling
        Mi = dMi.to_Matrix() / dMi.domain.to_sympy(den)

    return Mi

