
def test_exp_AccumBounds():
    assert exp(AccumBounds(1, 2)) == AccumBounds(E, E**2)

