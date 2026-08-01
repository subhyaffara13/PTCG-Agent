
def test_check_overflow_message():
    # Regression test for a bug where the overflow and underflow
    # messages were switched.
    with pytest.raises(sc.SpecialFunctionError, match="overflow"):
        with sc.errstate(all='raise'):
            # This should trigger an overflow:
            sc.yn(3, 1e-105)

