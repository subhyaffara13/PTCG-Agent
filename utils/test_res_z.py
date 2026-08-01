
def test_res_z():
    x = Symbol('x')

    assert res_z(3, 5, x) == 1
    assert res(3, 5, x) == res_q(3, 5, x) == res_z(3, 5, x)

