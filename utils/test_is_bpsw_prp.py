
def test_is_bpsw_prp():
    # invalid input
    raises(ValueError, lambda: is_bpsw_prp(0))

    # n = 1
    assert not is_bpsw_prp(1)

    # n is prime
    assert is_bpsw_prp(2)
    assert is_bpsw_prp(3)
    assert is_bpsw_prp(11)
    assert is_bpsw_prp(2**31-1)

