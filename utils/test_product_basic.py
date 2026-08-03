from typing import Union

def test_product_basic():
    H, T = 'H', 'T'
    unit_line = Interval(0, 1)
    d6 = FiniteSet(1, 2, 3, 4, 5, 6)
    d4 = FiniteSet(1, 2, 3, 4)
    coin = FiniteSet(H, T)

    square = unit_line * unit_line

    assert (0, 0) in square
    assert 0 not in square
    assert (H, T) in coin ** 2
    assert (.5, .5, .5) in (square * unit_line).flatten()
    assert ((.5, .5), .5) in square * unit_line
    assert (H, 3, 3) in (coin * d6 * d6).flatten()
    assert ((H, 3), 3) in coin * d6 * d6
    HH, TT = sympify(H), sympify(T)
    assert set(coin**2) == {(HH, HH), (HH, TT), (TT, HH), (TT, TT)}

    assert (d4*d4).is_subset(d6*d6)

    assert square.complement(Interval(-oo, oo)*Interval(-oo, oo)) == Union(
        (Interval(-oo, 0, True, True) +
         Interval(1, oo, True, True))*Interval(-oo, oo),
         Interval(-oo, oo)*(Interval(-oo, 0, True, True) +
                  Interval(1, oo, True, True)))

    assert (Interval(-5, 5)**3).is_subset(Interval(-10, 10)**3)
    assert not (Interval(-10, 10)**3).is_subset(Interval(-5, 5)**3)
    assert not (Interval(-5, 5)**2).is_subset(Interval(-10, 10)**3)

    assert (Interval(.2, .5)*FiniteSet(.5)).is_subset(square)  # segment in square

    assert len(coin*coin*coin) == 8
    assert len(S.EmptySet*S.EmptySet) == 0
    assert len(S.EmptySet*coin) == 0
    raises(TypeError, lambda: len(coin*Interval(0, 2)))

