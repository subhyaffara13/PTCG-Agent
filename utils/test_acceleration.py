
def test_acceleration():
    e = (1 + 1/n)**n
    assert round(richardson(e, n, 10, 20).evalf(), 10) == round(E.evalf(), 10)

    A = Sum(Integer(-1)**(k + 1) / k, (k, 1, n))
    assert round(shanks(A, n, 25).evalf(), 4) == round(log(2).evalf(), 4)
    assert round(shanks(A, n, 25, 5).evalf(), 10) == round(log(2).evalf(), 10)

