
def test_euler():
    assert euler(0) == 1
    assert euler(1) == 0
    assert euler(2) == -1
    assert euler(3) == 0
    assert euler(4) == 5
    assert euler(6) == -61
    assert euler(8) == 1385

    assert euler(20, evaluate=False) != 370371188237525

    n = Symbol('n', integer=True)
    assert euler(n) != -1
    assert euler(n).subs(n, 2) == -1

    assert euler(-1) == S.Pi / 2
    assert euler(-1, 1) == 2*log(2)
    assert euler(-2).evalf() == (2*S.Catalan).evalf()
    assert euler(-3).evalf() == (S.Pi**3 / 16).evalf()
    assert str(euler(2.3).evalf(n=10)) == '-1.052850274'
    assert str(euler(1.2, 3.4).evalf(n=10)) == '3.575613489'
    assert str(euler(I).evalf(n=10)) == '1.248446443 - 0.7675445124*I'
    assert str(euler(I, I).evalf(n=10)) == '0.04812930469 + 0.01052411008*I'

    assert euler(20).evalf() == 370371188237525.0
    assert euler(20, evaluate=False).evalf() == 370371188237525.0

    assert euler(n).rewrite(Sum) == euler(n)
    n = Symbol('n', integer=True, nonnegative=True)
    assert euler(2*n + 1).rewrite(Sum) == 0
    _j = Dummy('j')
    _k = Dummy('k')
    assert euler(2*n).rewrite(Sum).dummy_eq(
            I*Sum((-1)**_j*2**(-_k)*I**(-_k)*(-2*_j + _k)**(2*n + 1)*
                  binomial(_k, _j)/_k, (_j, 0, _k), (_k, 1, 2*n + 1)))

