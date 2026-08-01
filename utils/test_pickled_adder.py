
def test_pickled_adder():
    padder = pickle.dumps(adder)
    padd5 = pickle.loads(padder)(x)
    assert padd5(y) == x+y

