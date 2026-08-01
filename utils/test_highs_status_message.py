
def test_highs_status_message():
    res = linprog(1, method='highs')
    msg = "Optimization terminated successfully. (HiGHS Status 7:"
    assert res.status == 0
    assert res.message.startswith(msg)

    A, b, c, numbers, M = magic_square(6)
    bounds = [(0, 1)] * len(c)
    integrality = [1] * len(c)
    options = {"time_limit": 0.1}
    res = linprog(c=c, A_eq=A, b_eq=b, bounds=bounds, method='highs',
                  options=options, integrality=integrality)
    msg = "Time limit reached. (HiGHS Status 13:"
    assert res.status == 1
    assert res.message.startswith(msg)

    options = {"maxiter": 10}
    res = linprog(c=c, A_eq=A, b_eq=b, bounds=bounds, method='highs-ds',
                  options=options)
    msg = "Iteration limit reached. (HiGHS Status 14:"
    assert res.status == 1
    assert res.message.startswith(msg)

    res = linprog(1, bounds=(1, -1), method='highs')
    msg = "The problem is infeasible. (HiGHS Status 8:"
    assert res.status == 2
    assert res.message.startswith(msg)

    res = linprog(-1, method='highs')
    msg = "The problem is unbounded. (HiGHS Status 10:"
    assert res.status == 3
    assert res.message.startswith(msg)

    from scipy.optimize._linprog_highs import _highs_to_scipy_status_message
    status, message = _highs_to_scipy_status_message(58, "Hello!")
    msg = "The HiGHS status code was not recognized. (HiGHS Status 58:"
    assert status == 4
    assert message.startswith(msg)

    status, message = _highs_to_scipy_status_message(None, None)
    msg = "HiGHS did not provide a status code. (HiGHS Status None: None)"
    assert status == 4
    assert message.startswith(msg)

