
def test_X1():
    v, c = symbols('v c', real=True)
    assert (series(1/sqrt(1 - (v/c)**2), v, x0=0, n=8) ==
            5*v**6/(16*c**6) + 3*v**4/(8*c**4) + v**2/(2*c**2) + 1 + O(v**8))

