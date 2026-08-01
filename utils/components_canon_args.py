
def components_canon_args(components):
    numtyp = []
    prev = None
    for t in components:
        if t == prev:
            numtyp[-1][1] += 1
        else:
            prev = t
            numtyp.append([prev, 1])
    v = []
    for h, n in numtyp:
        if h.comm in (0, 1):
            comm = h.comm
        else:
            comm = TensorManager.get_comm(h.comm, h.comm)
        v.append((h.symmetry.base, h.symmetry.generators, n, comm))
    return v

