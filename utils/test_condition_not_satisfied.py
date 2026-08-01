
def test_condition_not_satisfied():
    iter_in = [0]
    assert index_satisfying(iter_in, lambda x: x > 0) == 1

