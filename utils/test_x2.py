
def test_X2():
    v, c = symbols('v c', real=True)
    s1 = series(1/sqrt(1 - (v/c)**2), v, x0=0, n=8)
    assert (1/s1**2).series(v, x0=0, n=8) == -v**2/c**2 + 1 + O(v**8)

