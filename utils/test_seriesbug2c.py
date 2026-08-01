
def test_seriesbug2c():
    w = Symbol("w", real=True)
    #more complicated case, but sin(x)~x, so the result is the same as in (1)
    e = (sin(2*w)/w)**(1 + w)
    assert e.series(w, 0, 1) == 2 + O(w)
    assert e.series(w, 0, 3) == 2 + 2*w*log(2) + \
        w**2*(Rational(-4, 3) + log(2)**2) + O(w**3)
    assert e.series(w, 0, 2).subs(w, 0) == 2

