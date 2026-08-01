
def test_issue_15124():
    omega = IndexedBase('omega')
    m, p = symbols('m p', cls=Idx)
    assert integrate(exp(x*I*(omega[m] + omega[p])), x, conds='none') == \
        -I*exp(I*x*omega[m])*exp(I*x*omega[p])/(omega[m] + omega[p])

