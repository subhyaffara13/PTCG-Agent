
def acot_fixed(a, prec, hyperbolic):
    """
    Compute acot(a) or acoth(a) for an integer a with binary splitting; see
    http://numbers.computation.free.fr/Constants/Algorithms/splitting.html
    """
    N = int(0.35 * prec/math.log(a) + 20)
    p, q, r = bsp_acot(a, 0,N, hyperbolic)
    return ((p+q)<<prec)//(q*a)

