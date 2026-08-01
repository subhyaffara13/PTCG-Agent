
def test_x0_working(solver, xp, batch_A, batch_b):
    # Easy problem
    A, b, x0 = _setup_random_system(xp, batch_A, batch_b)

    if solver is minres:
        kw = dict(rtol=1e-6)
    else:
        kw = dict(atol=0.0, rtol=1e-6)

    x, info = solver(A, b, **kw)
    assert info == 0

    _assert_success(A=A, x=x, b=b, xp=xp, rtol=1e-6)

    x, info = solver(A, b, x0=x0, **kw)
    assert info == 0
    _assert_success(A=A, x=x, b=b, xp=xp, rtol=1e-5)

