
def test_seriesbug2d():
    w = Symbol("w", real=True)
    e = log(sin(2*w)/w)
    assert e.series(w, n=5) == log(2) - 2*w**2/3 - 4*w**4/45 + O(w**5)

