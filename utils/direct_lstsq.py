
def direct_lstsq(a, b, cmplx=0):
    at = transpose(a)
    if cmplx:
        at = conjugate(at)
    a1 = dot(at, a)
    b1 = dot(at, b)
    return solve(a1, b1)

