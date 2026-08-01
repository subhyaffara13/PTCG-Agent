
def test_issue_24978():
    # Irreducible poly with negative leading coeff is normalized
    # (factor of -1 is extracted), before being stored as CRootOf.poly.
    f = -x**2 + 2
    r = CRootOf(f, 0)
    assert r.poly.as_expr() == x**2 - 2
    # An action that prompts calculation of an interval puts r.poly in
    # the cache.
    r.n()
    assert r.poly in rootoftools._reals_cache

