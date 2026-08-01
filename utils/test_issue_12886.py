
def test_issue_12886():
    m__1, l__1 = symbols('m__1, l__1')
    assert latex(m__1**2 + l__1**2) == \
        r'\left(l^{1}\right)^{2} + \left(m^{1}\right)^{2}'

