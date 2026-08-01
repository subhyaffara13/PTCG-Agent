
def test_V16():
    # Integral not calculated
    assert integrate(cos(5*x)*Ci(2*x), x) == Ci(2*x)*sin(5*x)/5 - (Si(3*x) + Si(7*x))/10

