
def test_list2numpy():
    assert (array([x**2, x]) == list2numpy([x**2, x])).all()

