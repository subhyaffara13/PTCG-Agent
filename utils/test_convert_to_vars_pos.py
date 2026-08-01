
def test_convert_to_varsPOS():
    assert _convert_to_varsPOS([0, 1, 0], [x, y, z]) == Or(x, Not(y), z)
    assert _convert_to_varsPOS([3, 1, 0], [x, y, z]) == Or(Not(y), z)

