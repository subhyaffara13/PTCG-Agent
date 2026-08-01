
def test_H1():
    assert simplify(2*2**n) == simplify(2**(n + 1))
    assert powdenest(2*2**n) == simplify(2**(n + 1))

