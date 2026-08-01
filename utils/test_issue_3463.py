
def test_issue_3463():
    w, i = symbols('w,i')
    r = log(5)/log(3)
    p = w**(-1 + r)
    e = 1/x*(-log(w**(1 + r)) + log(w + w**r))
    e_ser = -r*log(w)/x + p/x - p**2/(2*x) + O(w)
    assert e.nseries(w, n=1) == e_ser

