
def test_nonlinsolve_radical():
    assert nonlinsolve([sqrt(y) - x - z, y - 1], [x, y, z]) == {(1 - z, 1, z)}

