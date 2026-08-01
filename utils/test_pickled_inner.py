
def test_pickled_inner():
    add5 = adder(x)
    pinner = pickle.dumps(add5) #XXX: FAILS in pickle
    p5add = pickle.loads(pinner)
    assert p5add(y) == x+y

