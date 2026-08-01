
def test_solveset_real_log():
    assert solveset_real(log((x-1)*(x+1)), x) == \
        FiniteSet(sqrt(2), -sqrt(2))

