
def test_solve_lin_sys_2x2_one():
    domain, x1,x2 = ring("x1,x2", QQ)
    eqs = [x1 + x2 - 5,
           2*x1 - x2]
    sol = {x1: QQ(5, 3), x2: QQ(10, 3)}
    _sol = solve_lin_sys(eqs, domain)
    assert _sol == sol and all(s.ring == domain for s in _sol)

