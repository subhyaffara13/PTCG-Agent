
def test_nat_addsub_tdlike_scalar(obj):
    assert NaT + obj is NaT
    assert obj + NaT is NaT
    assert NaT - obj is NaT

