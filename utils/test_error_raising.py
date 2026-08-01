
def test_error_raising(errstate_lock):
    with errstate_lock:
        with special.errstate(all='raise'):
            assert_raises(special.SpecialFunctionError, special.iv, 1, 1e99j)

