
def test_bad_legacy_unary_ufunc_silent_errors():
    # Unary has a special scalar path right now, so test it explicitly.
    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error_unary(np.arange(3).astype(np.float64))

    with pytest.raises(RuntimeError, match=r"How unexpected :\)!"):
        ncu_tests.always_error_unary(1.5)

