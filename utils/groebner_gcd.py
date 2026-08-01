
def groebner_gcd(f, g):
    """Computes GCD of two polynomials using Groebner bases. """
    if f.ring != g.ring:
        raise ValueError("Values should be equal")
    domain = f.ring.domain

    if not domain.is_Field:
        fc, f = f.primitive()
        gc, g = g.primitive()
        gcd = domain.gcd(fc, gc)

    H = (f*g).quo([groebner_lcm(f, g)])

    if len(H) != 1:
        raise ValueError("Length should be 1")
    h = H[0]

    if not domain.is_Field:
        return gcd*h
    else:
        return h.monic()

