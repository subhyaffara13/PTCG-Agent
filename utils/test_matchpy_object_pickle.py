
def test_matchpy_object_pickle():
    if matchpy is None:
        return

    a1 = WildDot("a")
    a2 = pickle.loads(pickle.dumps(a1))
    assert a1 == a2

    a1 = WildDot("a", S(1))
    a2 = pickle.loads(pickle.dumps(a1))
    assert a1 == a2

    a1 = WildPlus("a", S(1))
    a2 = pickle.loads(pickle.dumps(a1))
    assert a1 == a2

    a1 = WildStar("a", S(1))
    a2 = pickle.loads(pickle.dumps(a1))
    assert a1 == a2

