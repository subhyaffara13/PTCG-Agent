
def test_truth_table():
    assert list(truth_table(And(x, y), [x, y], input=False)) == \
           [False, False, False, True]
    assert list(truth_table(x | y, [x, y], input=False)) == \
           [False, True, True, True]
    assert list(truth_table(x >> y, [x, y], input=False)) == \
           [True, True, False, True]
    assert list(truth_table(And(x, y), [x, y])) == \
           [([0, 0], False), ([0, 1], False), ([1, 0], False), ([1, 1], True)]

