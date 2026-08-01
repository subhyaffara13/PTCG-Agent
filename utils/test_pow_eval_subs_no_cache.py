
def test_pow_eval_subs_no_cache():
    # Tests pull request 9376 is working
    from sympy.core.cache import clear_cache

    s = 1/sqrt(x**2)
    # This bug only appeared when the cache was turned off.
    # We need to approximate running this test without the cache.
    # This creates approximately the same situation.
    clear_cache()

    # This used to fail with a wrong result.
    # It incorrectly returned 1/sqrt(x**2) before this pull request.
    result = s.subs(sqrt(x**2), y)
    assert result == 1/y

