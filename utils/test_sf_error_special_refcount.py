import sys

def test_sf_error_special_refcount():
    # Regression test for gh-16233.
    # Check that the reference count of scipy.special is not increased
    # when a SpecialFunctionError is raised.
    refcount_before = sys.getrefcount(sc)
    with sc.errstate(all='raise'):
        with pytest.raises(sc.SpecialFunctionError, match='domain error'):
            sc.ndtri(2.0)
    refcount_after = sys.getrefcount(sc)
    assert refcount_after == refcount_before

