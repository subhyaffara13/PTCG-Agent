
def test_seriesbug2b():
    w = Symbol("w")
    #test sin
    e = sin(2*w)/w
    assert e.nseries(w, 0, 3) == 2 - 4*w**2/3 + O(w**3)

