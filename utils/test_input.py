
def test_input():
    r = (2,3), Rational(2, 3), (Rational(2), Rational(3))
    for m in ["Greedy", "Graham Jewett", "Takenouchi", "Golomb"]:
        for i in r:
            d = egyptian_fraction(i, m)
            assert all(i.is_Integer for i in d)
            if m == "Graham Jewett":
                assert d == [3, 4, 12]
            else:
                assert d == [2, 6]
    # check prefix
    d = egyptian_fraction(Rational(5, 3))
    assert d == [1, 2, 6] and all(i.is_Integer for i in d)

