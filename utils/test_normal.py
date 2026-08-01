
def test_normal():
    x = symbols('x')
    e = Mul(S.Half, 1 + x, evaluate=False)
    assert e.normal() == e


def test_normal():
    serialized = dill.dumps(lambda x: x)

