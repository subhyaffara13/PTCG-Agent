
def test_reversed_reversedsign_property():
    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(x, y).reversed.reversedsign == f(x, y).reversedsign.reversed

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(-x, y).reversed.reversedsign == f(-x, y).reversedsign.reversed

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(x, -y).reversed.reversedsign == f(x, -y).reversedsign.reversed

    for f in (Eq, Ne, Ge, Gt, Le, Lt):
        assert f(-x, -y).reversed.reversedsign == \
            f(-x, -y).reversedsign.reversed

