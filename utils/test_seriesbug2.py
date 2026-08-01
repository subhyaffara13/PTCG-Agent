
def test_seriesbug2():
    w = Symbol("w")
    #simple case (1):
    e = ((2*w)/w)**(1 + w)
    assert e.nseries(w, 0, 1) == 2 + O(w, w)
    assert e.nseries(w, 0, 1).subs(w, 0) == 2

