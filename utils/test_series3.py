
def test_series3():
    w = Symbol("w", real=True)
    e = w**(-6)*(w**3*tan(w) - w**3*sin(w))
    assert e.nseries(w, n=8) == Integer(1)/2 + w**2/8 + 13*w**4/240 + 529*w**6/24192 + O(w**8)

