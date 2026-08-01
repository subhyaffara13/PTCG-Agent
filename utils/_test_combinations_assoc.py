
def _test_combinations_assoc():
    assert set(allcombinations((1,2,3), (a,b), True)) == \
        {(((1, 2), (3,)), (a, b)), (((1,), (2, 3)), (a, b))}

