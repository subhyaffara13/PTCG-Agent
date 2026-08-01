
def test_sum_of_four_squares():
    from sympy.core.random import randint

    # this should never fail
    n = randint(1, 100000000000000)
    assert sum(i**2 for i in sum_of_four_squares(n)) == n

    # error
    raises(ValueError, lambda: sum_of_four_squares(-1))

    for n in range(1000):
        result = sum_of_four_squares(n)
        assert len(result) == 4
        assert all(r >= 0 for r in result)
        assert sum(r**2 for r in result) == n
        assert list(result) == sorted(result)

