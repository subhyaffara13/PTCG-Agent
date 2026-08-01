
def test_nosols():
    # diophantine should sympify eq so that these are equivalent
    assert diophantine(3) == set()
    assert diophantine(S(3)) == set()

