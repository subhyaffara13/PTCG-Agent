
def test_inf_Range_len():
    raises(ValueError, lambda: len(Range(0, oo, 2)))
    assert Range(0, oo, 2).size is S.Infinity
    assert Range(0, -oo, -2).size is S.Infinity
    assert Range(oo, 0, -2).size is S.Infinity
    assert Range(-oo, 0, 2).size is S.Infinity

