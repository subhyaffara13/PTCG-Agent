
def _eigenvals_dict(
    M, error_when_incomplete=True, simplify=False, **flags):
    iblocks = M.strongly_connected_components()
    all_eigs = {}
    is_dom = M._rep.domain in (ZZ, QQ)
    for b in iblocks:

        # Fast path for a 1x1 block:
        if is_dom and len(b) == 1:
            index = b[0]
            val = M[index, index]
            all_eigs[val] = all_eigs.get(val, 0) + 1
            continue

        block = M[b, b]

        if isinstance(simplify, FunctionType):
            charpoly = block.charpoly(simplify=simplify)
        else:
            charpoly = block.charpoly()

        eigs = roots(charpoly, multiple=False, **flags)

        if sum(eigs.values()) != block.rows:
            try:
                eigs = dict(charpoly.all_roots(multiple=False))
            except NotImplementedError:
                if error_when_incomplete:
                    raise MatrixError(eigenvals_error_message)
                else:
                    eigs = {}

        for k, v in eigs.items():
            if k in all_eigs:
                all_eigs[k] += v
            else:
                all_eigs[k] = v

    if not simplify:
        return all_eigs
    if not isinstance(simplify, FunctionType):
        simplify = _simplify
    return {simplify(key): value for key, value in all_eigs.items()}

