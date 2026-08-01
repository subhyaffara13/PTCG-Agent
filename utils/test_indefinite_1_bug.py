
def test_indefinite_1_bug():
    assert integrate((b + t)**(-a), t, meijerg=True) == -b*(1 + t/b)**(1 - a)/(a*b**a - b**a)

