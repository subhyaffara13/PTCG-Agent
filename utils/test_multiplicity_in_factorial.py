
def test_multiplicity_in_factorial():
    n = fac(1000)
    for i in (2, 4, 6, 12, 30, 36, 48, 60, 72, 96):
        assert multiplicity(i, n) == multiplicity_in_factorial(i, 1000)

