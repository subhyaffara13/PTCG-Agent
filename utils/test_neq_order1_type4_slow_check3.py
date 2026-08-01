
def test_neq_order1_type4_slow_check3():
    eqs, sol = _neq_order1_type4_slow3()
    assert checksysodesol(eqs, sol) == (True, [0, 0])

