
def test_expand_mul():
    # part of issue 20597
    e = Mul(2, 3, evaluate=False)
    assert e.expand() == 6

    e = Mul(2, 3, 1/x, evaluate=False)
    assert e.expand() == 6/x
    e = Mul(2, R(1, 3), evaluate=False)
    assert e.expand() == R(2, 3)

