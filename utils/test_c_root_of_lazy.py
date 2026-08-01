
def test_CRootOf_lazy():
    # irreducible poly with both real and complex roots:
    f = Poly(x**3 + 2*x + 2)

    # real root:
    CRootOf.clear_cache()
    r = CRootOf(f, 0)
    # Not yet in cache, after construction:
    assert r.poly not in rootoftools._reals_cache
    assert r.poly not in rootoftools._complexes_cache
    r.evalf()
    # In cache after evaluation:
    assert r.poly in rootoftools._reals_cache
    assert r.poly not in rootoftools._complexes_cache

    # complex root:
    CRootOf.clear_cache()
    r = CRootOf(f, 1)
    # Not yet in cache, after construction:
    assert r.poly not in rootoftools._reals_cache
    assert r.poly not in rootoftools._complexes_cache
    r.evalf()
    # In cache after evaluation:
    assert r.poly in rootoftools._reals_cache
    assert r.poly in rootoftools._complexes_cache

    # composite poly with both real and complex roots:
    f = Poly((x**2 - 2)*(x**2 + 1))

    # real root:
    CRootOf.clear_cache()
    r = CRootOf(f, 0)
    # In cache immediately after construction:
    assert r.poly in rootoftools._reals_cache
    assert r.poly not in rootoftools._complexes_cache

    # complex root:
    CRootOf.clear_cache()
    r = CRootOf(f, 2)
    # In cache immediately after construction:
    assert r.poly in rootoftools._reals_cache
    assert r.poly in rootoftools._complexes_cache

