
def _eigenvects_DOM(M, **kwargs):
    DOM = DomainMatrix.from_Matrix(M, field=True, extension=True)
    DOM = DOM.to_dense()

    if DOM.domain != EX:
        rational, algebraic = dom_eigenvects(DOM)
        eigenvects = dom_eigenvects_to_sympy(
            rational, algebraic, M.__class__, **kwargs)
        eigenvects = sorted(eigenvects, key=lambda x: default_sort_key(x[0]))

        return eigenvects
    return None

