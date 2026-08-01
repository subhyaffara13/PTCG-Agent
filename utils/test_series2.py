
def test_series2():
    w = Symbol("w", real=True)
    x = Symbol("x", real=True)
    e = w**(-2)*(w*exp(1/x - w) - w*exp(1/x))
    assert e.nseries(w, n=4) == -exp(1/x) + w*exp(1/x)/2 - w**2*exp(1/x)/6 + w**3*exp(1/x)/24 + O(w**4)

