
def test_polygamma_expansion():
    # A. & S., pa. 259 and 260
    assert polygamma(0, 1/x).nseries(x, n=3) == \
        -log(x) - x/2 - x**2/12 + O(x**3)
    assert polygamma(1, 1/x).series(x, n=5) == \
        x + x**2/2 + x**3/6 + O(x**5)
    assert polygamma(3, 1/x).nseries(x, n=11) == \
        2*x**3 + 3*x**4 + 2*x**5 - x**7 + 4*x**9/3 + O(x**11)

