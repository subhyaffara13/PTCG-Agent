
def test_issue_21532():
    f = Function('f')
    g = Function('g')
    FUNC_F, FUNC_G = symbols('FUNC_F, FUNC_G')
    assert f(x).count_ops(visual=True) == FUNC_F
    assert g(x).count_ops(visual=True) == FUNC_G

