
def test_neq_order1_type4_slow3():
    eqs, sol = _neq_order1_type4_slow3()
    assert dsolve_system(eqs, simplify=False, doit=False) == [sol]

