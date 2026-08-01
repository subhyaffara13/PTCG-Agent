
def test_solve_lin_sys_3x4_one():
    domain, x1,x2,x3 = ring("x1,x2,x3", QQ)
    eqs = [x1 + 2*x2 + 3*x3,
           2*x1 - x2 + x3,
           3*x1 + x2 + x3,
           5*x2 + 2*x3]
    sol = {x1: 0, x2: 0, x3: 0}
    assert solve_lin_sys(eqs, domain) == sol

