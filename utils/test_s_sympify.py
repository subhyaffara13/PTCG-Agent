
def test_S_sympify():
    assert S(1)/2 == sympify(1)/2 == S.Half
    assert (-2)**(S(1)/2) == sqrt(2)*I

