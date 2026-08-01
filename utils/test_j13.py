
def test_J13():
    a = symbols('a', integer=True, negative=False)
    assert chebyshevt(a, -1) == (-1)**a

