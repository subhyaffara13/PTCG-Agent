
def test_W19():
    # Integral not calculated
    # Expected result is (cos 7 - 1)/7   [Gradshteyn and Ryzhik 6.782(3)]
    assert integrate(Ci(x)*besselj(0, 2*sqrt(7*x)), (x, 0, oo)) == (cos(7) - 1)/7

