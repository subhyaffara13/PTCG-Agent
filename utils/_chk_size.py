
def _chk_size(a, b):
    a = ma.asanyarray(a)
    b = ma.asanyarray(b)
    (na, nb) = (a.size, b.size)
    if na != nb:
        raise ValueError("The size of the input array should match!"
                         f" ({na} <> {nb})")
    return (a, b, na)

