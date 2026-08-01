
def test_bad_legacy_gufunc_silent_errors(x1):
    # Verify that an exception raised in a gufunc loop propagates correctly.
    # The signature of always_error_gufunc is '(i),()->()'.
    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error_gufunc(x1, 0.0)

