
def test_convert_to_varsSOP():
    assert _convert_to_varsSOP([0, 1, 0], [x, y, z]) == And(Not(x), y, Not(z))
    assert _convert_to_varsSOP([3, 1, 0], [x, y, z]) == And(y, Not(z))

