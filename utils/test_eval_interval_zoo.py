
def test_eval_interval_zoo():
    # Test that limit is used when zoo is returned
    assert Si(1/x)._eval_interval(x, S.Zero, S.One) == -pi/2 + Si(1)

