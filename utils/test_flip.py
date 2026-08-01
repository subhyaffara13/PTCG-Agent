
def test_flip():
    def f(a, b):
        return a, b

    assert flip(f, 'a', 'b') == ('b', 'a')


def test_flip():
    flip = pickle.loads(pickle.dumps(toolz.functoolz.flip))
    assert flip is toolz.functoolz.flip
    g1 = flip(f)
    g2 = pickle.loads(pickle.dumps(g1))
    assert g1(1, 2) == g2(1, 2) == f(2, 1)
    g1 = flip(f)(1)
    g2 = pickle.loads(pickle.dumps(g1))
    assert g1(2) == g2(2) == f(2, 1)

