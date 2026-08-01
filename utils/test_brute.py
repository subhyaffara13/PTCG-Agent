
def test_brute():
    tree = ([inc, dec], square)
    fn = brute(tree, lambda x: -x)

    assert fn(2) == (2 + 1)**2
    assert fn(-2) == (-2 - 1)**2

    assert brute(inc)(1) == 2

