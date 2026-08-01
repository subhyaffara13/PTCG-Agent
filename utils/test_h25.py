
def test_H25():
    e = (x - 2*y**2 + 3*z**3) ** 20
    assert factor(expand(e)) == e

