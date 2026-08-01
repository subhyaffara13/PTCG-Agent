
def test_J12():
    assert simplify(chebyshevt(1008, x) - 2*x*chebyshevt(1007, x) + chebyshevt(1006, x)) == 0

