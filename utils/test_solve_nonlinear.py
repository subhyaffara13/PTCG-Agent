
def test_solve_nonlinear():
    assert solve(x**2 - y**2, x, y, dict=True) == [{x: -y}, {x: y}]
    assert solve(x**2 - y**2/exp(x), y, x, dict=True) == [{y: -x*sqrt(exp(x))},
                                                          {y: x*sqrt(exp(x))}]

