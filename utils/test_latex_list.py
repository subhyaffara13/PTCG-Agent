
def test_latex_list():
    ll = [Symbol('omega1'), Symbol('a'), Symbol('alpha')]
    assert latex(ll) == r'\left[ \omega_{1}, \  a, \  \alpha\right]'

