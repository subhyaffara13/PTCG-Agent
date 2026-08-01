
def test_pickling_polys_rings():
    # NOTE: can't use protocols < 2 because we have to execute __new__ to
    # make sure caching of rings works properly.

    from sympy.polys.rings import PolyRing

    ring = PolyRing("x,y,z", ZZ, lex)

    for c in (PolyRing, ring):
        check(c, exclude=[0, 1])

    for c in (ring.dtype, ring.one):
        check(c, exclude=[0, 1], check_attr=False) # TODO: Py3k

