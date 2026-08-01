
def test_sort_key():
    assert MatAdd(Y, X).doit().args == add(Y, X).doit().args == (X, Y)

