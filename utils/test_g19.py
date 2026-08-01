
def test_G19():
    s = symbols('s', integer=True, positive=True)
    it = cf_i((exp(1/s) - 1)/(exp(1/s) + 1))
    assert list(islice(it, 5)) == [0, 2*s, 6*s, 10*s, 14*s]

