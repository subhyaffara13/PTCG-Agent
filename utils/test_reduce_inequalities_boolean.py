
def test_reduce_inequalities_boolean():
    assert reduce_inequalities(
        [Eq(x**2, 0), True]) == Eq(x, 0)
    assert reduce_inequalities([Eq(x**2, 0), False]) == False
    assert reduce_inequalities(x**2 >= 0) is S.true  # issue 10196

