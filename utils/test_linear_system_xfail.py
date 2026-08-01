
def test_linear_system_xfail():
    # https://github.com/sympy/sympy/issues/6420
    M = Matrix([[0,    15.0, 10.0, 700.0],
                [1,    1,    1,    100.0],
                [0,    10.0, 5.0,  200.0],
                [-5.0, 0,    0,    0    ]])

    assert solve_linear_system(M, x, y, z) == {x: 0, y: -60.0, z: 160.0}

