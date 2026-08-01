
def _eigenvals_list(
    M, error_when_incomplete=True, simplify=False, **flags):
    iblocks = M.strongly_connected_components()
    all_eigs = []
    is_dom = M._rep.domain in (ZZ, QQ)
    for b in iblocks:

        # Fast path for a 1x1 block:
        if is_dom and len(b) == 1:
            index = b[0]
            val = M[index, index]
            all_eigs.append(val)
            continue

        block = M[b, b]

        if isinstance(simplify, FunctionType):
            charpoly = block.charpoly(simplify=simplify)
        else:
            charpoly = block.charpoly()

        eigs = roots(charpoly, multiple=True, **flags)

        if len(eigs) != block.rows:
            try:
                eigs = charpoly.all_roots(multiple=True)
            except NotImplementedError:
                if error_when_incomplete:
                    raise MatrixError(eigenvals_error_message)
                else:
                    eigs = []

        all_eigs += eigs

    if not simplify:
        return all_eigs
    if not isinstance(simplify, FunctionType):
        simplify = _simplify
    return [simplify(value) for value in all_eigs]

