
def test_minimum_maximum():
    for MM, mm in zip([Min, Max], [minimum, maximum]):
        ref = MM(x, y, z)
        m = mm(x, y, z)
        assert m != ref
        assert m.rewrite(MM) == ref

