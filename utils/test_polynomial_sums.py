
def test_polynomial_sums():
    assert summation(n**2, (n, 3, 8)) == 199
    assert summation(n, (n, a, b)) == \
        ((a + b)*(b - a + 1)/2).expand()
    assert summation(n**2, (n, 1, b)) == \
        ((2*b**3 + 3*b**2 + b)/6).expand()
    assert summation(n**3, (n, 1, b)) == \
        ((b**4 + 2*b**3 + b**2)/4).expand()
    assert summation(n**6, (n, 1, b)) == \
        ((6*b**7 + 21*b**6 + 21*b**5 - 7*b**3 + b)/42).expand()

