
def test_boundary_ProductSet():
    open_square = Interval(0, 1, True, True) ** 2
    assert open_square.boundary == (FiniteSet(0, 1) * Interval(0, 1)
                                  + Interval(0, 1) * FiniteSet(0, 1))

    second_square = Interval(1, 2, True, True) * Interval(0, 1, True, True)
    assert (open_square + second_square).boundary == (
                FiniteSet(0, 1) * Interval(0, 1)
              + FiniteSet(1, 2) * Interval(0, 1)
              + Interval(0, 1) * FiniteSet(0, 1)
              + Interval(1, 2) * FiniteSet(0, 1))

