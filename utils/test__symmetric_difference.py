from typing import Set, Union

def test_SymmetricDifference():
    A = FiniteSet(0, 1, 2, 3, 4, 5)
    B = FiniteSet(2, 4, 6, 8, 10)
    C = Interval(8, 10)

    assert SymmetricDifference(A, B, evaluate=False).is_iterable is True
    assert SymmetricDifference(A, C, evaluate=False).is_iterable is None
    assert FiniteSet(*SymmetricDifference(A, B, evaluate=False)) == \
        FiniteSet(0, 1, 3, 5, 6, 8, 10)
    raises(TypeError,
        lambda: FiniteSet(*SymmetricDifference(A, C, evaluate=False)))

    assert SymmetricDifference(FiniteSet(0, 1, 2, 3, 4, 5), \
            FiniteSet(2, 4, 6, 8, 10)) == FiniteSet(0, 1, 3, 5, 6, 8, 10)
    assert SymmetricDifference(FiniteSet(2, 3, 4), FiniteSet(2, 3, 4 ,5)) \
            == FiniteSet(5)
    assert FiniteSet(1, 2, 3, 4, 5) ^ FiniteSet(1, 2, 5, 6) == \
            FiniteSet(3, 4, 6)
    assert Set(S(1), S(2), S(3)) ^ Set(S(2), S(3), S(4)) == Union(Set(S(1), S(2), S(3)) - Set(S(2), S(3), S(4)), \
            Set(S(2), S(3), S(4)) - Set(S(1), S(2), S(3)))
    assert Interval(0, 4) ^ Interval(2, 5) == Union(Interval(0, 4) - \
            Interval(2, 5), Interval(2, 5) - Interval(0, 4))


def test_SymmetricDifference():
    assert str(SymmetricDifference(Interval(2, 3), Interval(3, 4),evaluate=False)) == \
           'SymmetricDifference(Interval(2, 3), Interval(3, 4))'

