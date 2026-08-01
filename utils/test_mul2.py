
def test_mul2():
    """When this fails, remove things labelled "2-arg hack"
    1) remove special handling in the fallback of subs that
    was added in the same commit as this test
    2) remove the special handling in Mul.flatten
    """
    assert (2*(x + 1)).is_Mul

