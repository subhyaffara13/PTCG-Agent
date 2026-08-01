
def test_xreplace():
    assert OperationsOnlyMatrix([[1, x], [x, 4]]).xreplace({x: 5}) == \
           Matrix([[1, 5], [5, 4]])
    assert OperationsOnlyMatrix([[x, 2], [x + y, 4]]).xreplace({x: -1, y: -2}) == \
           Matrix([[-1, 2], [-3, 4]])


def test_xreplace():
    assert Matrix([[1, x], [x, 4]]).xreplace({x: 5}) == \
        Matrix([[1, 5], [5, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).xreplace({x: -1, y: -2}) == \
        Matrix([[-1, 2], [-3, 4]])
    for cls in classes:
        assert Matrix([[2, 0], [0, 2]]) == cls.eye(2).xreplace({1: 2})


def test_xreplace():
    assert Matrix([[1, x], [x, 4]]).xreplace({x: 5}) == \
        Matrix([[1, 5], [5, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).xreplace({x: -1, y: -2}) == \
        Matrix([[-1, 2], [-3, 4]])
    for cls in all_classes:
        assert Matrix([[2, 0], [0, 2]]) == cls.eye(2).xreplace({1: 2})


def test_xreplace():
    assert b21.xreplace({b2: b1}) == Basic(b1, b1)
    assert b21.xreplace({b2: b21}) == Basic(b21, b1)
    assert b3.xreplace({b2: b1}) == b2
    assert Basic(b1, b2).xreplace({b1: b2, b2: b1}) == Basic(b2, b1)
    assert Atom(b1).xreplace({b1: b2}) == Atom(b1)
    assert Atom(b1).xreplace({Atom(b1): b2}) == b2
    raises(TypeError, lambda: b1.xreplace())
    raises(TypeError, lambda: b1.xreplace([b1, b2]))
    for f in (exp, Function('f')):
        assert f.xreplace({}) == f
        assert f.xreplace({}, hack2=True) == f
        assert f.xreplace({f: b1}) == b1
        assert f.xreplace({f: b1}, hack2=True) == b1


def test_xreplace():
    e = Mul(2, 1 + x, evaluate=False)
    assert e.xreplace({}) == e
    assert e.xreplace({y: x}) == e

