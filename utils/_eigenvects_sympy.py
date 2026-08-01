
def _eigenvects_sympy(M, iszerofunc, simplify=True, **flags):
    eigenvals = M.eigenvals(rational=False, **flags)

    # Make sure that we have all roots in radical form
    for x in eigenvals:
        if x.has(CRootOf):
            raise MatrixError(
                "Eigenvector computation is not implemented if the matrix have "
                "eigenvalues in CRootOf form")

    eigenvals = sorted(eigenvals.items(), key=default_sort_key)
    ret = []
    for val, mult in eigenvals:
        vects = _eigenspace(M, val, iszerofunc=iszerofunc, simplify=simplify)
        ret.append((val, mult, vects))
    return ret

