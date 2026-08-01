
def test_slots():
    assert dill.pickles(Y)
    assert dill.pickles(y)
    assert dill.pickles(Y.y)
    assert dill.copy(y).y == value
    assert dill.copy(Y2(value)).y == value

